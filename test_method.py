import numpy as np
import math

ceki = np.array([[154,150,169,65],
                [70,96,136,141],
                [130,150,95,99],
                [146,99,124,109]])

# ceki = np.array([[154,150,169,100,154,150,169,100],
#                 [171,136,96,141,171,136,96,141],
#                 [146,130,95,99,146,130,95,99],
#                 [150,99,124,109,150,99,124,109],
#                 [154,150,169,100,154,150,169,100],
#                 [171,136,96,141,171,136,96,141],
#                 [146,130,95,99,146,130,95,99],
#                 [150,99,124,109,150,99,124,109]])

# print(cek[1][1])
# dwt = np.array([[0]*height]*width)
def go_dct(cek):
    height,width = np.shape(cek)
    t = np.zeros((height,width))
    n = height
    for i in range(height):
        for j in range(width):
            if i==0:
                t[i][j] = 1/math.sqrt(n)
            else:
                t[i][j] = (math.sqrt(2/n))*math.cos(((2*j)+1)*i*math.pi/(2*n))

    tt = t.transpose()
    dct = np.matmul(t,cek)
    dct = np.matmul(dct,tt)

    return dct

def go_idct(cek):
    height,width = np.shape(cek)
    t = np.zeros((height,width))
    n = height
    for i in range(height):
        for j in range(width):
            if i==0:
                t[i][j] = 1/math.sqrt(n)
            else:
                t[i][j] = (math.sqrt(2/n))*math.cos(((2*j)+1)*i*math.pi/(2*n))

    tt = t.transpose()
    idct = np.matmul(tt,cek)
    idct = np.matmul(idct,t)

    return idct


def go_dwt(cek):
    height,width = np.shape(cek)
    dwt = np.zeros((height,width))
    # print(height, " ", width)
    x = int(width/2)
    for i in range(height):
        x = int(width/2)
        # while x > 1:
        for j in range(x):
            # print(i, " ", j, "==",cek[i][j*2]," ", cek[i][(j*2)+1])
            summ = int(cek[i][j*2]) + int(cek[i][(j*2)+1])
            diff = int(cek[i][j*2]) - int(cek[i][(j*2)+1])
            dwt[i][j] = summ/2
            dwt[i][j+x] = diff/2
        # x = int(x/2)
    # print(dwt)
    # print("====")
    cek2 = dwt.transpose()
    dwt = np.zeros((height,width))
    # print(cek2)
    for i in range(height):
        # x = int(width/2)
        # while x > 1:
        for j in range(x):
            # print(i, " ", j, "==",cek2[i][j*2]," ", cek2[i][(j*2)+1])
            summ = int(cek2[i][j*2]) + int(cek2[i][(j*2)+1])
            diff = int(cek2[i][j*2]) - int(cek2[i][(j*2)+1])
            dwt[i][j] = summ
            dwt[i][j+x] = diff
        # x = int(x/2)
    dwt = dwt.transpose()
    cA = dwt[0:x,0:x]
    cH = dwt[x:width,0:x]
    cV = dwt[0:x,x:height]
    cD = dwt[x:width,x:height]
    # print(dwt)
    return cA, (cH, cV, cD)

def go_idwt(coeffs):
    cA, (cH, cV, cD) = coeffs
    x,y = np.shape(cA)
    # print(x, " ",y)
    height = x*2
    width = y*2
    idwt = np.zeros((height,width))
    cek = np.zeros((height,width))
    cek[0:x,0:y] = cA
    cek[x:width,0:y] = cH
    cek[0:x,y:height] = cV
    cek[x:width,y:height] = cD
    # print(cek)
    cek = cek.transpose()
    for i in range(height):
        x = int(width/2)
        # while x > 1:
        for j in range(x):
            summ = int(cek[i][j]) + int(cek[i][j+x])
            diff = int(cek[i][j]) - int(cek[i][j+x])
            idwt[i][j*2] = summ/2
            idwt[i][(j*2)+1] = diff/2
        # x = int(x/2)
    # print(idwt)
    # print("====")
    cek2 = idwt.transpose()
    idwt = np.zeros((height,width))
    # print(cek2)
    for i in range(height):
        x = int(width/2)
        # while x > 1:
        for j in range(x):
            # print(i, " ", j, "==",cek2[i][j*2]," ", cek2[i][j+x])
            summ = int(cek2[i][j]) + int(cek2[i][j+x])
            diff = int(cek2[i][j]) - int(cek2[i][j+x])
            idwt[i][j*2] = summ
            idwt[i][(j*2)+1] = diff
        # x = int(x/2)
    # print(idwt)
    return idwt

# # # phaseDWT = np.round(go_dwt(ceki)).astype(int)
# phaseDWT = go_dwt(ceki)
# print(phaseDWT)
# # print(np.round(phaseDWT).astype(int))
# # # phaseIDWT = np.round(go_idwt(phaseDWT)).astype(int)
# phaseIDWT = go_idwt(phaseDWT)
# print(phaseIDWT)

# phaseDCT = go_dct(ceki)
# print(np.round(phaseDCT).astype(int))
# phaseIDCT = go_idct(phaseDCT)
# print(np.round(phaseIDCT).astype(int))