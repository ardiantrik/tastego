import cv2
import numpy as np
from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2
import os
import math

UPLOAD_FOLDER = os.getcwd() + '/assets/'

coverImage = cv2.imread(UPLOAD_FOLDER + "/cek/DWT-lenna.png",1)
wm = cv2.imread(UPLOAD_FOLDER + "/cek/lenna.png",1)

mse = np.mean((coverImage - wm) ** 2 )
print("MSE : " + str(mse))
if mse == 0:
    psnr = 100
else:
    PIXEL_MAX = 255.0
    psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

print("PSNR : " + str(psnr))