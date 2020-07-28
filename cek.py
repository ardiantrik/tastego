import cv2
import numpy as np
from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2, dwt, idwt

# cek = np.array([[154,150,169,100],
#                 [171,136,96,141],
#                 [146,130,95,99],
#                 [150,99,124,109]])
cek = np.array([[154,150,169,100,154,150,169,100],
                [171,136,96,141,171,136,96,141],
                [146,130,95,99,146,130,95,99],
                [150,99,124,109,150,99,124,109],
                [154,150,169,100,154,150,169,100],
                [171,136,96,141,171,136,96,141],
                [146,130,95,99,146,130,95,99],
                [150,99,124,109,150,99,124,109]])

# # cek = np.array([[154,150],
# #                 [171,136]])

# cek_dct = cv2.dct(np.float32(cek))
# # cek_dct = np.uint8(dct(cek))
# cek_dct = np.round(cek_dct).astype(int)
# print(cek_dct)
# print("==================")

# cek_idct = cv2.idct(np.float32(cek_dct))
# # cek_idct = np.uint8(idct(cek_dct))

# print(np.round(cek_idct).astype(int))


cA, (cH, cV, cD) = dwt2(cek, 'haar')  
coeffs = cA, (cH, cV, cD)
print(cD)

# cek3 = np.array([[88,80],
#                  [70,77]])

klmt = 'MANTAppu JIWA'
x,y = np.shape(cD)
z=0
for i in range(x):
    for j in range(y):
        if i==0 and j==0:
            cD[i][j] = len(klmt)
        else:
            if z<len(klmt):
                cD[i][j] = ord(klmt[z])
                z = z+1
            else:
                break
    

# cD = cek3
coeffs = cA, (cH, cV, cD)

print("==================")
cek_idwt = idwt2(coeffs, 'haar')

print(np.uint8(cek_idwt))
cA, (cH, cV, cD) = dwt2(cek_idwt, 'haar')  
print("==================")
z=0
kont = ''
for i in range(x):
    for j in range(y):
        if i == 0 and j == 0:
            jumlah = cD[i][j].astype(int)
            print(jumlah)
        else:
            if z<jumlah:
                kont = kont+ chr(cD[i][j].astype(int))
                z = z+1
                print(z)
            else:
                break


print(kont)
        





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
