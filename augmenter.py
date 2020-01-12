import cv2
import os
import numpy as np
from skimage.util import random_noise
from random import seed
from random import randint
from datetime import datetime

seed(datetime.now())

def rot(img, angle):
    rows,cols,ch = img.shape
    # cols-1 and rows-1 are the coordinate limits.
    M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),angle ,1)
    return cv2.warpAffine(img,M,(cols,rows))
 
f = open('species.txt', 'r')
species = f.read().split("\n")
dirs = os.listdir( 'Data/' )

for each in species:
    for dir in dirs:
        if ' '.join(each.split(' - ')) in dir:
            print(each)
            data = os.listdir('Data/'+dir+'/clean/')
            count = len(data)
            for img in data:
                image = cv2.imread('Data/'+dir+'/clean/'+img)
                for i in range(1, 8):
                    out = rot(image, 45*i)
                    cv2.imwrite('Data/'+dir+'/clean/'+str(count)+'.png', out)
                    count += 1
            print('...')