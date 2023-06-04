def growRegion(lastplaced, img):
    dic = {}            # temporary dictionary to store information of function call
    newimg = img.copy()
    new_placed = []         # temparary array that stores pixels assigned this iteration
    cont = False            # boolean value that determins whether more pixels are able to be assigned on the next iteration
    
    for point in lastplaced:            # checking 4 adjacent pixels of all pixels assigned last iteration
        if(newimg[point[0]+1][point[1]] < 40):
            newimg[point[0]+1][point[1]] = 128
            new_placed.append((point[0]+1, point[1]))
            cont = True
        if(newimg[point[0]-1][point[1]] < 40):
            newimg[point[0]-1][point[1]] = 128
            new_placed.append((point[0]-1, point[1]))
            cont = True
        if(newimg[point[0]][point[1]+1] < 40):
            newimg[point[0]][point[1]+1] = 128
            new_placed.append((point[0], point[1]+1))
            cont = True
        if(newimg[point[0]][point[1]-1] < 40):
            newimg[point[0]][point[1]-1] = 128
            new_placed.append((point[0], point[1]-1))
            cont = True
        
    dic["image"] = newimg
    dic["points"] = new_placed
    dic["cont"] = cont
    
    return dic
    