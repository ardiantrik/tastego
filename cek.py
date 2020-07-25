import cv2
import numpy as np
from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2

cek = np.array([[154,150,169,100],
                [171,136,96,141],
                [146,130,95,99],
                [150,99,124,109]])

# cek_dct = np.uint8(cv2.dct(np.float32(cek)))
# #cek_dct = dct(cek)

# print(cek_dct)
# print("==================")

# cek_idct = np.uint8(cv2.idct(np.float32(cek_dct)))
# #cek_idct = idct(cek_dct)

# print(cek_idct)


cA, (cH, cV, cD) = dwt2(cek, 'haar')  
coeffs = cA, (cH, cV, cD)
print(cA)

print("==================")
cek_idwt = idwt2(coeffs, 'haar')

print(np.uint8(cek_idwt))