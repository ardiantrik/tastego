import cv2
import numpy as np
# from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2
import os
import math

UPLOAD_FOLDER = os.getcwd() + '/assets/'

coverImage = cv2.imread(UPLOAD_FOLDER + "/cek/lenna.png",1)
wm = cv2.imread(UPLOAD_FOLDER + "/cek/LSB-lenna.png",1)
# (x,y,z) = wm.shape
# wm = cv2.resize(wm,(400,400))
coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
wm = cv2.cvtColor(wm, cv2.COLOR_BGR2RGB)
# (thresh, bw) = cv2.threshold(wm, 127, 255, cv2.THRESH_BINARY)
# r1, g1, b1 = cv2.split(wm)
# x,y = np.shape(bw)

# print(x, " ",y)
# print(thresh)
# # dr1 = cv2.dct(np.float32(r1))
# r2 = np.around(cv2.dct(np.float32(r1))).astype(int)
# x,y = np.shape(r2)
# print(x, " ", y)
# print(r2)
# dr1 = np.around(cv2.idct(np.float32(r2))).astype(int)
# x,y = np.shape(dr1)
# print(x, " ", y)
# print(dr1)
# for i in range(x):
#     for j in range(y):
#         if (dr1[i,j]>255) or (dr1[i,j]<0):
#             print(dr1[i,j])
#             dr1[i,j] = 255
# counterss = 0
# for i in range(x):
#     for j in range(y):
#         if (dr1[i,j]>255) or (dr1[i,j]<0):
#             counterss += 1

# print(counterss)
# img = cv2.merge((b1,g1,dr1))
# cek = cv2.imwrite(UPLOAD_FOLDER + "/cek/cekdct/DCTR2-lenna.png", img)


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
# print(coverImage)
# print("========")
# print(wm)
# r1, g1, b1 = cv2.split(cekcoba)


# cek1 = np.array([[100,226,60,150],
#                 [20,60,40,30],
#                 [50,90,70,82],
#                 [74,66,90,58]])

# cek2 = np.array([[90,227,30,110],
#                 [90,60,50,40],
#                 [70,20,70,82],
#                 [14,56,90,54]])

cek2 = np.array([[155,150,169,65],
                [70,96,135,141],
                [130,150,95,99],
                [146,100,124,109]])

cek1 = np.array([[154,150,169,65],
                [70,96,136,141],
                [130,150,95,99],
                [146,99,124,109]])

# r1, g1, b1 = cv2.split(coverImage)
# r2, g2, b2 = cv2.split(wm)
# # print(r1)
# # print("========")
# # print(r2)
# # print("========")
# # print(np.sum(np.subtract(r1.astype(int),r2.astype(int))))
# # rs = np.sum(np.subtract(r1.astype(int),r2.astype(int)))
# # gs = np.sum(np.subtract(g1.astype(int),g2.astype(int)))
# # bs = np.sum(np.subtract(b1.astype(int),b2.astype(int)))
# rs = np.subtract(r1.astype(int),r2.astype(int))**2
# gs = np.subtract(g1.astype(int),g2.astype(int))**2
# bs = np.subtract(b1.astype(int),b2.astype(int))**2
# cekkin = np.subtract(cek1.astype(int),cek2.astype(int))**2
# # print(np.subtract(cek1.astype(int),cek2.astype(int)))
# print(np.sum(np.sqrt(abs(cekkin))))
# # eucDist = math.sqrt((rs**2)+(gs**2)+(bs**2))
# # print(eucDist)

jarak = np.sum((np.subtract(cek1.astype(int),cek2.astype(int)))**2)
print(jarak)
eucDist = math.sqrt(jarak)
print(eucDist)


# mse = np.mean((coverImage - wm) ** 2 )
# mse = np.mean((cek1 - cek2) ** 2 )
# print((cek1 - cek2) ** 2 )
# print("MSE : " + str(mse))
# if mse == 0:
#     psnr = 100
# else:
#     PIXEL_MAX = 255.0
#     psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

# print("PSNR : " + str(psnr))