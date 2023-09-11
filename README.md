# ImageSegment
Basic image segmentation script for DICOM images using OpenCV edge detection


# TO USE THE PROGRAM #

- add folders "DICOMs", "DICOMsjpg", and "regions"
- insert ".dcm" files into "DICOMs" folder
- if the images contain a region of interest, set "RegionOI" to "True" on line 7, otherwise, set to "False"
- run the script
- results will be written into "regions" folder
- note: depending on the colours, clarity, and other factors of the images, values such as thresh1, and thresh2 may need to be changed to best process the images

# METHODOLOGY #

- the program processea a DICOM image 
- the processed image is passed into an edge detection function from OpenCV library
- a new image with the edges shown in white is returned
- the edge image is further processed to connect edges and improve clarity
- a region growing algorithm is then used to locate the coordinates of each pixel in group of pixels surrounded by an edge, this group of pixels is called a region
- regions with less than 21 pixels are ignored
- the regions are iterated through and each region is rendered onto a new blank image with the original RGB value

# ASSUMPTIONS #

- all images in "DICOMs" folder are of ".dcm" format
- image returned from edge detection is greyscaled

# LIMITATIONS #
- certain colours used to mark ROIs are not detected well, for example rendered
- clarity of images will affect performance of program
- edges of regions are often cut off when rendered due to method used to connect edges
- certain regions may contain nothing of interest, but the program still classifies them as a region, for example a black background
