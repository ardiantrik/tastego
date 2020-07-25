import cv2
import numpy as np
from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2

cek = np.array([[154,150,169,100],
                [171,136,96,141],
                [146,130,95,99],
                [150,99,124,109]])

# cek = np.array([[154,150],
#                 [171,136]])

cek_dct = cv2.dct(np.float32(cek))
# cek_dct = np.uint8(dct(cek))
cek_dct = np.round(cek_dct).astype(int)
print(cek_dct)
print("==================")

cek_idct = cv2.idct(np.float32(cek_dct))
# cek_idct = np.uint8(idct(cek_dct))

print(np.round(cek_idct).astype(int))


# cA, (cH, cV, cD) = dwt2(cek, 'haar')  
# coeffs = cA, (cH, cV, cD)
# print(cA)

# print("==================")
# cek_idwt = idwt2(coeffs, 'haar')

# print(np.uint8(cek_idwt))