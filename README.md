# slide_colour_palette
Colour palette extractor for WSI images from the "Enhancing Liver Fibrosis Measurement: Deep Learning and Uncertainty Analysis Across Multi-Centre Cohorts" paper.
https://www.medrxiv.org/content/10.1101/2025.05.12.25326981v1

NB: the code relies on Otsu thresholding for identification of tissue area.
In lightly stained cases the theshold may need adjustment.
The method may fail if there are substantial artefacts in slide background.
