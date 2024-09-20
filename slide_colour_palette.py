import os
from pathlib import Path
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray, rgb2hsv, rgb2lab
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from colorthief import ColorThief
plt.rcParams['figure.dpi'] = 150
from openslide import OpenSlide  # can use wsireader instead


def save_thumbnail(slide_path, o, erase_background=True):
	"""
    Generates and saves a thumbnail image from a slide, with optional background erasure.

    This function opens a whole-slide image, generates a thumbnail at a specified level, 
    and optionally erases the background using Otsu's thresholding. The thumbnail is then 
    saved as a PNG file.

    Args:
        slide_path (str): Path to the whole-slide image file.
        o (str): Output directory path where the thumbnail will be saved.
        erase_background (bool, optional): Whether to erase the background from the thumbnail.
        								   The background needs to be erased for the color 
        								   palette extraction to work.
                                           Default is True.

    Returns:
        None: The function saves the thumbnail image to the specified output directory.
    """


    filename = str(Path(slide_path).stem)
    slide = OpenSlide(slide_path)
    level = 5  # adjust to obtain a thumbnail size image
    dims = slide.level_dimensions[level]
    im = slide.get_thumbnail(dims)

    if erase_background:
        greyscale_im = rgb2gray(im)
        threshold = threshold_otsu(greyscale_im)
        mask = greyscale_im > threshold
        im = im + mask[:,:,None]
        im[im > 1] = 1

    im = (im * 255).astype(np.uint8) 
        
    file_name = o + filename + '.png'
    imsave(file_name, im)


def get_primary_LAB_values(thumbnails, color_index=0):
	"""
    Extracts primary LAB color values from a list of image thumbnails.

    This function takes a list of image thumbnails, extracts the most dominant color 
    (or a specified color from the palette) for each thumbnail, converts these colors 
    from RGB to LAB color space, and returns the LAB values along with the RGB values.

    Args:
        thumbnails (list): A list of image paths or image objects from which to extract colors.
        color_index (int, optional): The index of the color in the palette to use. 
                                      Default is 0 (most dominant color).

    Returns:
        tuple: A tuple containing four elements:
            - L (list): The L* values of the LAB color space.
            - A (list): The a* values of the LAB color space.
            - B (list): The b* values of the LAB color space.
            - RGB (numpy.ndarray): The RGB values of the extracted colors, normalized to [0, 1].
    """
    
    L = []
    A = []
    B = []
    RGB = []
    
    for thumbnail in thumbnails:
        color_thief = ColorThief(thumbnail)
        palette = color_thief.get_palette(color_count=3, quality=10)
        r = palette[color_index][0]
        g = palette[color_index][1]
        b = palette[color_index][2]
        [l, ast, bst] = rgb2lab(np.asarray([r,g,b])/255)
        L.append(l)
        A.append(ast)
        B.append(bst)
        RGB.append((r,g,b))  # this is used for plotting
        
    return L, A, B, np.asarray(RGB)/255


def plot_cohort_stain_distribution(thumbnails, dataset_name, stain):
	"""
    Plots the distribution of a stain in a cohort using LAB color space and saves the plot as an image.

    This function takes a list of thumbnail images, extracts their primary LAB color values, 
    and creates a 3D scatter plot of these values. The plot is saved to a file named 
    based on the dataset and stain provided.

    Args:
        thumbnails (list): A list of image thumbnails to be analyzed.
        dataset_name (str): The name of the dataset being analyzed, used for labeling the output plot.
        stain (str): The type of stain used in the images, also used for labeling the output plot.

    Returns:
        None: The function saves the plot as an image file and displays it.
    """


    print(len(thumbnails))
    L, A, B, RGB = get_primary_LAB_values(thumbnails)
        
    fig = plt.figure(figsize=(9,9))

    ax = fig.add_subplot(111, projection='3d');
    ax.scatter(A, B, L, c=RGB, s=20, alpha=0.9)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.set_xlabel('a*', fontsize=22)
    ax.set_ylabel('b*', fontsize=22)
    ax.set_zlabel('L*', fontsize=22)
    ax.set_title(dataset_name,fontsize=24)

    file_name = './plots/' + f'{dataset_name}_{stain}_background_erased_LAB.png'
    plt.savefig(file_name, dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=0, metadata=None)
    plt.show()



def plot_combined_cohort_stain_distribution(datasets, dataset_names, stains):
"""
    Plots the combined distribution of stain colors across multiple datasets in LAB color space.

    This function processes multiple datasets, extracting the primary LAB color values from 
    thumbnail images associated with different stains. It then creates a 3D scatter plot 
    representing the combined color distribution for each stain across all datasets.

    Args:
        datasets (list): A list of dataset paths, each containing a directory of thumbnail images.
        dataset_names (list): A list of names corresponding to each dataset, used for labeling.
        stains (list): A list of stain types to process and plot.

    Returns:
        None: The function saves each combined cohort plot as an image file and displays it.
    """


for stain in stains:
    
    L_global = []
    A_global = []
    B_global = []
    RGB_global = []
    
    staintext = stain
    if staintext == 'HE':
        staintext = 'H&E'
    
    for i, dataset in enumerate(datasets):

        thumbnails = glob(dataset + f'Thumbnails/{stain}/*.png')
        L,A,B, RGB = get_primary_LAB_values(thumbnails)
        L_global.extend(L)
        A_global.extend(A)
        B_global.extend(B)
        RGB_global.extend(RGB)
        
    fig = plt.figure(figsize=(9,9))

    ax = fig.add_subplot(111, projection='3d');
    ax.scatter(A_global, B_global, L_global, c=RGB_global, s=20, alpha=0.9)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.set_xlabel('a*', fontsize=22)
    ax.set_ylabel('b*', fontsize=22)
    ax.set_zlabel('L*', fontsize=22)
    ax.set_title('Combined cohort ' + staintext,fontsize=24)

    file_name = './plots/' + f'all_datasets_{stain}_background_erased_LAB.png'
    plt.savefig(file_name, dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=0, metadata=None)
    plt.show()
