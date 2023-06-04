import cv2 as cv
import numpy as np
from pydicom import dcmread
from os import listdir, remove
from growRegion import growRegion

RegionOI = False            # variable to set porgram to Region of Interest Mode

if (RegionOI):              
    thresh1, thresh2 = 250, 350         # differen edge detection thresholds depending on mode
else: 
    thresh1, thresh2 = 0, 170

for file in listdir("ImageSeg/DICOMs"):         # iterate through all files in folder
    to_read = "ImageSeg/DICOMs/" + file
    
    dicom = dcmread(to_read)            # opening .dcm files using pydicom
    pixels = dicom.pixel_array          # fetching pixel data as numpy array, allows conversion to .jpg
    
    file = file.replace(".dcm", ".jpg")
    
    write_to = "ImageSeg/DICOMsjpg/" + file
    cv.imwrite(write_to , pixels)           # conversion to .jpg to open and use in OpenCV library
    
    to_read = "ImageSeg/DICOMsjpg/" + file
    img = cv.imread(to_read)
    original = img.copy()           # creating a copy of the original image to copy RGB values from later
    if (RegionOI == False):         
        img = cv.convertScaleAbs(img, 0, 4)         # a blur and brightness increase is applied, not needed if ROIs are marked
        img = cv.GaussianBlur(img, (9,9),0)

    img = cv.Canny(img, thresh1, thresh2)           # applying edge detection
    
    remove(to_read)         # removing the .jpg copy of the .dcm image because it is no longer needed

    x = 0           # variables to track x and y coordinates while iterating through each pixel of edge image
    y = 0

    dimensions = img.shape          # retrieving dimensions of image as a tuple

    img = cv.GaussianBlur(img, (5,5),0)         # pre processing for region growing
    img = cv.convertScaleAbs(img, 0, 3)

    regions = []            # dynamic array to store all regions

    for pixel_number in range(dimensions[1]*dimensions[0]):         # iterating through pixels of the image
        if(x == dimensions[1]):         # updating the y coodinate accordingly
            x = 0
            y+=1
        if (img[y][x] < 40):            # if the pixel currently indexed has a greyscaled colout value of under 40, start growing the region
            seeds = [(y,x)]         # array that stores the pixels indexed on last iteration         
            img[y][x] = 128         # setting the greyscale colour value to 128 if the pixel is assigned a region
            cont = True
            temp = seeds            # initalizing a temporary array to store all pixel coordinates of the region
            while (cont):
                data = growRegion(seeds, img)           # calling region growing function
                img = data["image"]
                seeds = data["points"]
                cont = data["cont"]
                temp+=seeds             # adding the last assigned pixels to the temporary array        
            regions.append(temp)            # adding the temporary array to the array of total regions
        x+=1

    count=0 
    for region in regions:          # iterating over the regions to render each one onto a new blank image
        if (len(region) > 20):          # regions with less than 21 pixels are ignored
            count+=1
            
            towrite = "ImageSeg/regions/" + file + "_" + str(count) + ".jpg"
            
            template = np.zeros((dimensions[0],dimensions[1],3), np.uint8)          # initializing blank image
            for pixel in region:
                template[pixel[0]][pixel[1]] = original[pixel[0]][pixel[1]]         # rendering each pixel in the region with the RGB value of the original image
            cv.imwrite(towrite, template) 