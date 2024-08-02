import os
from slide_colour_palette import plot_cohort_stain_distribution, plot_combined_cohort_stain_distribution

# add paths to your slide folders
calm_root_dir = 'path/to/slide/folder'
hepatica_root_dir = 'path/to/slide/folder'
prev_root_dir = 'path/to/slide/folder'
uk_aih_root_dir= 'path/to/slide/folder'

# make a list of folder paths
datasets = [calm_root_dir, hepatica_root_dir, prev_root_dir, uk_aih_root_dir]
# make a list of cohort names as you want them displayed in figures
dataset_names = ['CALM', 'HepaT1ca', 'PREV', 'UK-AIH']
# add names of stainings in your cohorts
stains = ['HE', 'PSR']

# make directories for slide thumbnails
for dataset in datasets:
    for stain in stains:
        if not os.path.exists(dataset + 'Thumbnails'):
            os.makedirs(dataset + 'Thumbnails')
        if not os.path.exists(dataset + f'Thumbnails/{stain}'):
            os.makedirs(dataset + f'Thumbnails/{stain}')


# save thumbnails for each of your cohorts
# you may need to adjust thumbnail size inside the save_thumbnail function depending on your 
# slide file types and sizes

o = prev_root_dir + 'Thumbnails/HE/'
for slide_path in prev_he_slides:
    save_thumbnail(slide_path, o, erase_background=True)

# plot the distribution of H&E slide colours from the PREV cohort
prev_thumbnails = 'prev_root_dir/Thumbnails'
plot_cohort_stain_distribution(prev_thumbnails, 'PREV', 'HE')

# plot the colour distribution(s) for the combined cohort
plot_combined_cohort_stain_distribution(datasets, dataset_names, stains)