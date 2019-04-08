import numpy as np
import os
import lossFunctions as lf
import cv2
import re
from struct import unpack

def load_data(path,train=True):
    imgl_list = []
    imgr_list = []
    pfm_img_list = []
    trains = os.listdir(path)
    for t in trains:
        imgl_list.append(cv2.imread(path+t+'\\im0.png',0))
        imgr_list.append(cv2.imread(path+t+'\\im1.png',0))
        if train==True:
            pfm_img_list.append(load_pfm(path+t+'\\disp0GT.pfm'))
    if train==True:
        return imgl_list, imgr_list, pfm_img_list
    else:
    	return imgl_list, imgr_list

def image_disparity(Il,Ir,distance,w=None):
    (r,c) = Il.shape
    result = np.zeros((r,c))
    for x in range(w,r-w):
        for y in range(w,c-w):
            disp = 0
            dist = distance(x,y,w,Il,Ir,0)
            for d in range(1,101):
                dt = distance(x,y,w,Il,Ir,-d)
                if dt<dist:
                    dist = dt
                    disp = d
            result[x][y] = disp
    return result

def load_pfm(file):
    # Adopted from https://stackoverflow.com/questions/48809433/read-pfm-format-in-python
    with open(file, "rb") as f:
        # Line 1: PF=>RGB (3 channels), Pf=>Greyscale (1 channel)
        type = f.readline().decode('latin-1')
        if "PF" in type:
            channels = 3
        elif "Pf" in type:
            channels = 1
        else:
            sys.exit(1)
        # Line 2: width height
        line = f.readline().decode('latin-1')
        width, height = re.findall('\d+', line)
        width = int(width)
        height = int(height)
        # Line 3: +ve number means big endian, negative means little endian
        line = f.readline().decode('latin-1')
        BigEndian = True
        if "-" in line:
            BigEndian = False
        # Slurp all binary data
        samples = width * height * channels;
        buffer = f.read(samples * 4)
        # Unpack floats with appropriate endianness
        if BigEndian:
            fmt = ">"
        else:
            fmt = "<"
        fmt = fmt + str(samples) + "f"
        img = unpack(fmt, buffer)
    return img

if __name__=='__main__':
	imgl_list, imgr_list, pfm_img_list = load_data("MiddEval3\\trainingQ\\",True)
	samples = len(imgr_list)
	#Squared distance
	squared_distance = 0
	for sam in range(samples):
		result = image_disparity(imgl_list[sam],imgr_list[sam], lf.squared_distance, w=1)
		squared_distance+=np.sqrt(((result - pfm_img_list[sam]) ** 2).mean())
		print(sam)
	squared_distance/=samples
	print('Average Squared distance:', squared_distance)
	#absolute distance
	abs_distance = 0
	for sam in range(samples):
		result = image_disparity(imgl_list[sam],imgr_list[sam], lf.abs_difference, w=1)
		abs_distance+=np.sqrt(((result - pfm_img_list[sam]) ** 2).mean())
	abs_distance/=samples
	print('Average Absolute distance:', squared_distance)
