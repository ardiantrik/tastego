import cv2
import numpy as np
from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2, dwt, idwt

quant = np.array([[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE
                    [12,12,14,19,26,58,60,55],    # required for DCT
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

# cek = np.array([[154,150,169,100],
#                 [171,136,96,141],
#                 [146,130,95,99],
#                 [150,99,124,109]])

# cek = np.array([[154,150,169,65],
#                 [70,96,136,141],
#                 [130,150,95,99],
#                 [146,99,124,109]])

# cek = np.array([[100,50,60,150],
#                 [20,60,40,30],
#                 [50,90,70,82],
#                 [74,66,90,58]])

# cek = np.array([[255,255,255,255],
#                 [255,255,170,255],
#                 [255,150,255,255],
#                 [255,255,255,255]])

cek = np.array([[154,150,169,100,154,150,169,100],
                [171,136,96,141,171,136,96,141],
                [146,130,95,99,146,130,95,99],
                [150,99,124,109,150,99,124,109],
                [154,150,169,100,154,150,169,100],
                [171,136,96,141,171,136,96,141],
                [146,130,95,99,146,130,95,99],
                [150,99,124,109,150,99,124,109]])

# print(cek[0:4,4:7])

# cek = np.array([[154,150],
#                 [171,136]])

# cek_dct = cv2.dct(np.float32(cek))
# # cek_dct = np.uint8(cek_dct)
# # cek_dct = np.uint8(dct(cek))
# # cek_dct = np.around(cek_dct).astype(int)
# cek_dct = np.around(cek_dct, 1)
# print(cek_dct)
# print("==================")
# cekdct = np.around(cek_dct).astype(int)
# print(cekdct)
# # # cekdct[0][2] = cekdct[0][2]+1
# # # cekdct[0][1] = cekdct[0][1]+1
# # # cekdct[0][0] = cekdct[0][0]+1
# # cekdct[0] = cekdct[0]+1
# # # cekdct[2] = cekdct[2]+1
# # # cekdct[4] = cekdct[4]+1
# # cekdct[7] = cekdct[7]+1
# # print("==================")
# # print(cekdct)
# print("==================")

# cek_idct = cv2.idct(np.float32(cekdct))
# # # cek_idct = np.uint8(idct(cek_dct))
# cek_idct = np.around(cek_idct, 1)
# print(cek_idct)
# cekidct = np.around(cek_idct).astype(int)
# print(cekidct)
# cek_dct = cv2.dct(np.float32(cekidct))
# cek_dct = np.around(cek_dct, 1)
# cekdct = np.around(cek/quant).astype(int)
cekdct = (cek/quant).astype(int)
print(cekdct)
# print("==================")

# cA, (cH, cV, cD) = dwt2(cek, 'haar')  
# coeffs = cA, (cH, cV, cD)
# print(np.round(cD).astype(int))

# print("==================")
# cek_idwt = idwt2(coeffs, 'haar')
# print(np.round(cek_idwt).astype(int))

# # cek3 = np.array([[88,80],
# #                  [70,77]])

# klmt = 'MANTAppu JIWA'
# x,y = np.shape(cA)
# z=0
# for i in range(x):
#     for j in range(y):
#         if i==0 and j==0:
#             cA[i][j] = len(klmt)
#         else:
#             if z<len(klmt):
#                 cA[i][j] = ord(klmt[z])
#                 z = z+1
#             else:
#                 break
    

# # cD = cek3
# coeffs = cA, (cH, cV, cD)

# print("==================")
# cek_idwt = idwt2(coeffs, 'haar')

# print(np.uint8(cek_idwt))
# cA, (cH, cV, cD) = dwt2(cek_idwt, 'haar')  
# print("==================")
# z=0
# kont = ''
# for i in range(x):
#     for j in range(y):
#         if i == 0 and j == 0:
#             jumlah = cA[i][j].astype(int)
#             print(jumlah)
#         else:
#             if z<jumlah:
#                 kont = kont+ chr(cA[i][j].astype(int))
#                 z = z+1
#                 print(z)
#             else:
#                 break


# print(kont)
        





# klmt = 'MANTAB JIWA'
# hit = len(klmt)
# kontainer = ''
# for i in range(hit):
#     kontainer = kontainer + f'{ord(klmt[i]):08b}'

# cek = '{0:08b}'.format(ord('A'))
# cek2 = f'{6:08b}'

# print(kontainer)
# # print(len(kontainer))
# kkont = list(kontainer)
# (cA, cD) =  dwt(kkont, 'db2', 'smooth')
# new_kont = np.round(idwt(cA, cD, 'db2', 'smooth')).astype(int)
# print(new_kont)

# x=1
# kont2 = ''
# kontainer = ''
# for i in range(len(new_kont)):
#     # print(i)
#     kont2 = kont2 + str(new_kont[i])
#     if x%8 == 0:
#         # print(kont2)
#         kontainer = kontainer + chr(int(kont2,2))
#         kont2 = ''
#     x = x+1
# print(kontainer)

# mata = np.array([[1,6],
#                 [4,3]])

# matb = np.array([[2,7],
#                  [1,4]])

# print(mata*matb)