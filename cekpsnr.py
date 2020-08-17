import cv2
import numpy as np
# from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2
import os
import math

UPLOAD_FOLDER = os.getcwd() + '/assets/'

# coverImage = cv2.imread(UPLOAD_FOLDER + "/cek/lenna.png",1)
wm = cv2.imread(UPLOAD_FOLDER + "/cek/lenna.png",1)

wm = cv2.cvtColor(wm, cv2.COLOR_BGR2RGB)
r1, g1, b1 = cv2.split(wm)
x,y = np.shape(r1)
print(x, " ", y)
print(r1)
# dr1 = cv2.dct(np.float32(r1))
r2 = np.around(cv2.dct(np.float32(r1))).astype(int)
x,y = np.shape(r2)
print(x, " ", y)
print(r2)
dr1 = np.around(cv2.idct(np.float32(r2))).astype(int)
x,y = np.shape(dr1)
print(x, " ", y)
print(dr1)
for i in range(x):
    for j in range(y):
        if (dr1[i,j]>255) or (dr1[i,j]<0):
            print(dr1[i,j])
            dr1[i,j] = 255
counterss = 0
for i in range(x):
    for j in range(y):
        if (dr1[i,j]>255) or (dr1[i,j]<0):
            counterss += 1

print(counterss)
img = cv2.merge((b1,g1,dr1))
cek = cv2.imwrite(UPLOAD_FOLDER + "/cek/cekdct/DCTR2-lenna.png", img)


# x,y = np.shape(r1)
# print(x,y)
# i=0
# for i in range((int(x/8))*8):
#     for j in range((int(y/8))*8):
# while i<(int(x/8))*8:
#     j=0
#     while j<(int(y/8))*8:
#         r3 = r1[i:i+8,j:j+8]
#         print(r3)
#         print(np.shape(r3))
#         j = j+8
#     i = i+8

# print(wm)        
# cekcoba = (coverImage-wm)
# print(cekcoba)
# mse = np.mean((coverImage - wm) ** 2 )
# print("MSE : " + str(mse))
# if mse == 0:
#     psnr = 100
# else:
#     PIXEL_MAX = 255.0
#     psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

# print("PSNR : " + str(psnr))