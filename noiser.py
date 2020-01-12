import cv2
import numpy as np
from skimage.util import random_noise
from random import seed
from random import randint
from datetime import datetime

seed(datetime.now())

def rot(img):
    rows,cols,ch = img.shape
    # cols-1 and rows-1 are the coordinate limits.
    M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),randint(0, 359) ,1)
    return cv2.warpAffine(img,M,(cols,rows))

def warp(img):
    rows,cols,ch = img.shape
    pts1 = np.float32([[randint(0, 399),randint(0, 399)],[randint(0, 399),randint(0, 399)],[randint(0, 399),randint(0, 399)],[randint(0, 399),randint(0, 399)]])
    pts2 = np.float32([[randint(0, 399),randint(0, 399)],[randint(0, 399),randint(0, 399)],[randint(0, 399),randint(0, 399)],[randint(0, 399),randint(0, 399)]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    return cv2.warpPerspective(img,M,(400,400))

def rota(img):
    return rot(affine(img))

def rotw(img):
    return rot(warp(img))

switch = {
    0: rot,
    1: warp,
    2: rotw
}
 
# Load the image
img = cv2.imread("training/other/hand.png")
 
# Add salt-and-pepper noise to the image.
noise_img = random_noise(img, mode='s&p',amount=0.3)
 
# The above function returns a floating-point image
# on the range [0, 1], thus we changed it to 'uint8'
# and from [0,255]
noise_img = np.array(255*noise_img, dtype = 'uint8')

cv2.imwrite("training/other/temp.png", noise_img)

count = 0

img = cv2.imread("training/other/hand.png")

for i in range(277):
 
    out = switch[randint(0, 2)](img)
    cv2.imwrite("training/notButterflies/"+str(count)+".png", out)

    count += 1

img = cv2.imread("training/other/concrete.png")

for i in range(277):
 
    out = switch[randint(0, 2)](img)
    cv2.imwrite("training/notButterflies/"+str(count)+".png", out)

    count += 1

img = cv2.imread("training/other/leaves.png")

for i in range(276):
 
    out = switch[randint(0, 2)](img)
    cv2.imwrite("training/notButterflies/"+str(count)+".png", out)

    count += 1