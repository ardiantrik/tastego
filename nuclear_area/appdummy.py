import os
import base64
import cv2
import numpy as np
import PIL  
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, send_file
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime
from pywt import dwt2, idwt2
import math
import random
from test_method import *

encode_folder = "Encoded_image_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M"))
decode_folder= "Decoded_image_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M"))
UPLOAD_FOLDER = os.getcwd() + '/assets/'
RESULT_FOLDER = os.getcwd() + '/static/result/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','bmp', 'tif'}
quant = np.array([[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE
                    [12,12,14,19,26,58,60,55],    # required for DCT
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

#=====Method Section=====
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def go_upload(file_up,id):
    if file_up and allowed_file(file_up.filename):
        filename = secure_filename(file_up.filename)
        fixname = str(id) + filename
        file_up.save(os.path.join(app.config['UPLOAD_FOLDER'], fixname))
    
    return fixname

def go_psnr(cover_img,stego_img):
    dimensiCover = np.shape(cover_img)
    dimensiStego = np.shape(stego_img)
    if (dimensiCover[0]*dimensiCover[1]) != (dimensiStego[0]*dimensiStego[1]):
        mse = (dimensiCover[0]*dimensiCover[1])-(dimensiStego[0]*dimensiStego[1])
        # eucDist= "Beda Dimensi"
    else:
        mse = np.mean((cover_img - stego_img) ** 2 )

    if mse == 0:
        psnr = 100
    else:
        PIXEL_MAX = 255.0
        psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    return mse,psnr

def go_eucDist(cover_img,stego_img):
    dimensiCover = np.shape(cover_img)
    dimensiStego = np.shape(stego_img)
    if (dimensiCover[0]*dimensiCover[1]) != (dimensiStego[0]*dimensiStego[1]):
        eucDist= "Beda Dimensi"
    else:
        r1, g1, b1 = cv2.split(cover_img)
        r2, g2, b2 = cv2.split(stego_img)

        rs = np.sum(np.subtract(r1.astype(int),r2.astype(int)))
        gs = np.sum(np.subtract(g1.astype(int),g2.astype(int)))
        bs = np.sum(np.subtract(b1.astype(int),b2.astype(int)))

        eucDist = math.sqrt((rs**2)+(gs**2)+(bs**2))

    return eucDist

def newgo_encodeLSB(coverImage,kontainer):
    r1, g1, b1 = cv2.split(coverImage)
    print(coverImage)
    hit_kontainer = len(kontainer)
    height,width = np.shape(r1)
    index = 0
    row_stop = 0
    col_stop = 0
    for row in range(height):
        for col in range(width):
            for i in range(3):
                if index<hit_kontainer:
                    # print(index, " ", kontainer[index], " ",hit_kontainer)
                    if i == 0:    
                        rbit_temp = f'{r1[row][col]:08b}'
                        rbit_lsb = list(rbit_temp)
                        rbit_lsb[-1] = kontainer[index]
                        rbit_temp = ''.join(rbit_lsb)
                        r1[row][col] = int(rbit_temp,2)
                    elif i == 1:
                        gbit_temp = f'{g1[row][col]:08b}'
                        gbit_lsb = list(gbit_temp)
                        gbit_lsb[-1] = kontainer[index]
                        gbit_temp = ''.join(gbit_lsb)
                        g1[row][col] = int(gbit_temp,2)
                    elif i == 2:
                        bbit_temp = f'{b1[row][col]:08b}'
                        bbit_lsb = list(bbit_temp)
                        bbit_lsb[-1] = kontainer[index]
                        bbit_temp = ''.join(bbit_lsb)
                        b1[row][col] = int(bbit_temp,2)
                    index = index + 1

                # bit_temp = f'{px[row][col]:08b}'
                # bit_lsb = list(bit_temp)
                # bit_lsb[-1] = kontainer[index]
                # bit_temp = ''.join(bit_lsb)
                # px[row][col] = int(bit_temp,2)
                else:
                    row_stop = 1
                    col_stop = 1
                    break
            if col_stop != 0:
                break
        if row_stop != 0:
            break
    # print(px)
    img = cv2.merge((b1,g1,r1))
    print(img)
    return img

def go_encodeLSB(px,kontainer):
    hit_kontainer = len(kontainer)
    height,width = np.shape(px)
    index = 0
    row_stop = 0
    for row in range(height):
        for col in range(width):
            if index<hit_kontainer:
                bit_temp = f'{px[row][col]:08b}'
                bit_lsb = list(bit_temp)
                bit_lsb[-1] = kontainer[index]
                bit_temp = ''.join(bit_lsb)
                px[row][col] = int(bit_temp,2)
                index = index + 1
            else:
                row_stop = 1
                break
        if row_stop != 0:
            break
    return px

def go_encodeAlt(px,kontainer):
    hit_kontainer = len(kontainer)
    height,width = np.shape(px)
    index = 0
    row_stop = 0
    for row in range(height):
        for col in range(width):
            if index<hit_kontainer:
                px[row][col] = ord(kontainer[index])
                index = index + 1
            else:
                row_stop = 1
                break
        if row_stop != 0:
            break
    # print(px)
    return px

def process_encode(cover_img, hidden_text):
    # baca gambar
    coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    cover = coverImage
    # convert BGR ke RGB
    coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    
    # preprocess pesan 
    hid = hidden_text+'~@&'
    hit_hidden = len(hid)
    
    # wadah buat pesan
    kontainer = ''
    kontainer16 = ''
    kontainer8 = ''
    kont_div = [['']]
    kont_div16 = [['']]
    kont_div8 = [['']]

    x = 0
    y = 0
    for i in range(hit_hidden):
        # persiapan pembagian bagian2 pesan
        kontainer = kontainer + f'{ord(hid[i]):08b}'
        kontainer16 = kontainer16 + f'{ord(hid[i]):08b}'
        kontainer8 = kontainer8 + f'{ord(hid[i]):08b}'
        
        # pesan dibagi menjadi 8-bit perbagian
        if i == 0:
            kont_div8[0] = kontainer8
        else:
            kont_div8.append(kontainer8)
        kontainer8 = ''

        # pesan dibagi menjadi 16-bit perbagian
        if (i+1)%2 == 0:
            if y == 0:
                kont_div16[y] = kontainer16
            else:
                kont_div16.append(kontainer16)
            kontainer16 = ''
            y = y + 1
    
    if kontainer16 != '':
        kont_div16.append(kontainer16)
    
    #LSB
    #membagi matriks citra sesuai ruang warna RGB
    r1, g1, b1 = cv2.split(coverImage)
    p,l = np.shape(r1)
    x = 0
    kont = ''
    # membagi pesan bila panjang pesan melebihi kapasitas cover
    if len(kontainer)>(p*l):
        for i in range(len(kontainer)):
            kont = kont + kontainer[i]
            if (i+1)%(p*l) == 0:
                if x == 0:
                    kont_div[x] = kont
                else:
                    kont_div.append(kont)
                kont = ''
                x = x + 1
                print(x)
        if kont != '':
            kont_div.append(kont)
    else:
        kont_div[x] = kontainer
    x = 0
    for i in range(3):
        if i== 0:
            px1 = r1
        elif i == 1:
            px1 = g1
        elif i == 2:
            px1 = b1

        if x<len(kont_div):
            # proses sisip
            px1 = go_encodeLSB(px1,kont_div[i])
            if i== 0:
                r1 = px1
            elif i == 1:
                g1 = px1
            elif i == 2:
                b1 = px1
            x = x + 1
        else:
            break
    # postprocess citra stego
    img = cv2.merge((b1,g1,r1))
    stegoLSB = img
    cek = cv2.imwrite(RESULT_FOLDER + encode_folder +"/LSB-" + cover_img, img)
    mse,psnr = go_psnr(cover,stegoLSB)
    print(mse, " ", psnr)
    dataLSB = {
        'file_name':"LSB-"+cover_img,
        'file_loc':"/static/result/"+ encode_folder +"/LSB-" + cover_img,
        'method':'LSB',
        'mse':mse,
        'psnr':psnr
    }

    #DCT
    r1, g1, b1 = cv2.split(coverImage)
    x,y = np.shape(r1)
    z=0

    for rgb in range(3):
        if rgb == 0:
            px1 = r1
        elif rgb == 1:
            px1 = g1
        elif rgb == 2:
            px1 = b1

        i=0
        while i<(int(x/8))*8:
            j=0
            while j<(int(y/8))*8:
                # mengambil pixel dengan dimensi 8x8
                px2 = px1[i:i+8,j:j+8]
                if z<len(kont_div8):
                    # proses DCT dan kuantisasi
                    # px2 = np.around(cv2.dct(np.float32(px2)), 1)
                    px2 = np.around(go_dct(np.float32(px2)), 1)
                    px2 = np.around(px2/quant).astype(int)

                    #mengambil 8-bit baru
                    #LF newpx = [px2[0][0],px2[0][1],px2[1][0],px2[2][0],px2[1][1],px2[0][2],px2[0][3],px2[1][2]]
                    newpx = [px2[0][3],px2[1][2],px2[2][1],px2[3][0],px2[4][0],px2[3][1],px2[2][2],px2[1][3]]
                    #HF newpx = [px2[7][7],px2[7][6],px2[6][7],px2[5][7],px2[6][6],px2[7][5],px2[6][5],px2[5][6]]
                    testpx = np.vstack((newpx,px2[1]))
                    # proses sisip pesan
                    testpx = go_encodeLSB(testpx,kont_div8[z])
                    
                    #mengembalikan 8-bit ke tempat asal
                    # px2[0][0],px2[0][1],px2[1][0],px2[2][0],px2[1][1],px2[0][2],px2[0][3],px2[1][2] = testpx[0] 
                    px2[0][3],px2[1][2],px2[2][1],px2[3][0],px2[4][0],px2[3][1],px2[2][2],px2[1][3] = testpx[0]
                    #HF px2[7][7],px2[7][6],px2[6][7],px2[5][7],px2[6][6],px2[7][5],px2[6][5],px2[5][6] = testpx[0]
                    
                    #proses IDCT dan kuantisasi
                    # px2 = np.around(cv2.idct(np.float32(px2*quant))).astype(int)
                    px2 = np.around(go_idct(np.float32(px2*quant))).astype(int)

                    if rgb== 0:
                        r1[i:i+8,j:j+8] = px2
                    elif rgb == 1:
                        g1[i:i+8,j:j+8] = px2
                    elif rgb == 2:
                        b1[i:i+8,j:j+8] = px2

                    z = z + 1
                else:
                    break
                j = j + 8
            i = i + 8
    
    # postprocess citra stego
    img = cv2.merge((b1,g1,r1))
    stegoDCT = img
    cek = cv2.imwrite(RESULT_FOLDER + encode_folder +"/DCT-" + cover_img, img)
    mse,psnr = go_psnr(cover,stegoDCT)
    print(mse, " ", psnr)
    dataDCT = {
        'file_name':"DCT-"+cover_img,
        'file_loc':"/static/result/"+ encode_folder +"/DCT-" + cover_img,
        'method':'DCT',
        'mse':mse,
        'psnr':psnr
    }

    #DWT
    r1, g1, b1 = cv2.split(coverImage)
    x,y = np.shape(r1)
    z=0
    
    for rgb in range(3):
        if rgb == 0:
            px1 = r1
        elif rgb == 1:
            px1 = g1
        elif rgb == 2:
            px1 = b1

        i=0
        while i<(int(x/8))*8:
            j=0
            while j<(int(y/8))*8:
                # mengambil pixel dengan dimensi 8x8
                px3 = px1[i:i+8,j:j+8]

                # proses DHWT
                # cA, (cH, cV, cD) = dwt2(px3, 'haar')  
                cA, (cH, cV, cD) = go_dwt(px3)  
                # pengambilan subband LH (cH)
                cH = np.around(cH).astype(int)
                if z<len(kont_div16):
                    # proses sisip pesan
                    cH = go_encodeLSB(cH,kont_div16[z])
                    # mengembalikkan subband LH
                    px3 = cA.astype(int),(cH.astype(int), cV.astype(int), cD.astype(int))
                    # proses IDHWT
                    # px3 = idwt2(px3, 'haar')
                    px3 = go_idwt(px3)
                    if rgb== 0:
                        r1[i:i+8,j:j+8] = px3
                    elif rgb == 1:
                        g1[i:i+8,j:j+8] = px3
                    elif rgb == 2:
                        b1[i:i+8,j:j+8] = px3

                    z = z + 1
                else:
                    break
                
                j = j + 8
            i = i + 8
    # postprocess citra stego
    img = cv2.merge((b1,g1,r1))
    stegoDWT = img
    cek = cv2.imwrite(RESULT_FOLDER + encode_folder +"/DWT-" + cover_img, img)
    mse,psnr = go_psnr(cover,stegoDWT)
    print(mse, " ", psnr)
    dataDWT = {
        'file_name':"DWT-"+cover_img,
        'file_loc':"/static/result/"+ encode_folder +"/DWT-" + cover_img,
        'method':'DWT',
        'mse':mse,
        'psnr':psnr
    }

    # KOMBINASI
    r1, g1, b1 = cv2.split(coverImage)
    x,y = np.shape(r1)
    z=0
    
    for rgb in range(3):
        if rgb == 0:
            px1 = r1
        elif rgb == 1:
            px1 = g1
        elif rgb == 2:
            px1 = b1

        i=0
        while i<(int(x/8))*8:
            j=0
            while j<(int(y/8))*8:
                # mengambil pixel dengan dimensi 8x8
                px3 = px1[i:i+8,j:j+8]
                if z<len(kont_div16):
                    # proses DHWT
                    # cA, (cH, cV, cD) = dwt2(px3, 'haar') 
                    cA, (cH, cV, cD) = go_dwt(px3)  
                    # proses DCT
                    # cH = np.round(cv2.dct(np.float32(cH))).astype(int)
                    cH = np.round(go_dct(np.float32(cH))).astype(int)
                    cH = np.around(cH).astype(int)
                    # proses sisip pesan
                    cH = go_encodeLSB(cH,kont_div16[z])
                    px3 = cA.astype(int),(cH.astype(int), cV.astype(int), cD.astype(int))
                    # proses IDWT
                    # px3 = idwt2(px3, 'haar')
                    px3 = go_idwt(px3)
                    if rgb== 0:
                        r1[i:i+8,j:j+8] = px3
                    elif rgb == 1:
                        g1[i:i+8,j:j+8] = px3
                    elif rgb == 2:
                        b1[i:i+8,j:j+8] = px3

                    z = z + 1
                else:
                    break
                
                j = j + 8
            i = i + 8
    # posprocessing citra stego
    img = cv2.merge((b1,g1,r1))
    stegoALL = img
    cek = cv2.imwrite(RESULT_FOLDER + encode_folder +"/ALL-" + cover_img, img)
    mse,psnr = go_psnr(cover,stegoALL)
    print(mse, " ", psnr)
    dataALL = {
        'file_name':"ALL-"+cover_img,
        'file_loc':"/static/result/"+ encode_folder +"/ALL-" + cover_img,
        'method':'ALL',
        'mse':mse,
        'psnr':psnr
    }

    result_data =[dataLSB,dataDCT,dataDWT,dataALL]
    return result_data

def newgo_decodeLSB(stegoImage):
    r1, g1, b1 = cv2.split(stegoImage)
    print(stegoImage)
    kontainer = ''
    stop_kontainer = ''
    height,width = np.shape(r1)
    index = 0
    row_stop = 0
    col_stop = 0
    stop_status = 0
    for row in range(height):
        for col in range(width):
            for i in range(3):
                if stop_status == 0:
                    if i == 0:    
                        rbit_temp = f'{r1[row][col]:08b}'
                        kontainer = kontainer + rbit_temp[-1]
                    elif i == 1:
                        gbit_temp = f'{g1[row][col]:08b}'
                        kontainer = kontainer + gbit_temp[-1]
                    elif i == 2:
                        bbit_temp = f'{b1[row][col]:08b}'
                        kontainer = kontainer +bbit_temp[-1]
                    index = index + 1
                # bit_temp = f'{px[row][col]:08b}'
                # kontainer = kontainer + bit_temp[-1]
                # index = index + 1

                    if index%8 == 0:
                        stop_kontainer = stop_kontainer + chr(int(kontainer,2))
                        if '~@&' in stop_kontainer:
                            stop_status = 999
                            row_stop = 1
                            print("STOP skuy")
                            break
                        else:
                            kontainer = ''
                else:
                    row_stop = 1
                    col_stop = 1
                    break
            if col_stop != 0:
                break
        if row_stop != 0:
            break
    # print(px)
    decodeLSB_result = stop_kontainer
    return decodeLSB_result

def go_decodeLSB(px):
    kontainer = ''
    stop_kontainer = ''
    # if np.ndim(px) == 1:
    #     height = 1
    #     width = len(px)
    # else:
    height,width = np.shape(px)
    index = 0
    row_stop = 0
    stop_status = 0
    for row in range(height):
        for col in range(width):
            if stop_status == 0:
                bit_temp = f'{px[row][col]:08b}'
                kontainer = kontainer + bit_temp[-1]
                index = index + 1

                if index%8 == 0:
                    stop_kontainer = stop_kontainer + chr(int(kontainer,2))
                    if '~@&' in stop_kontainer:
                        stop_status = 999
                        row_stop = 1
                        print("STOP skuy")
                        break
                    else:
                        kontainer = ''
            else:
                row_stop = 1
                break
        if row_stop != 0:
            break
    # print(px)
    decodeLSB_result = stop_kontainer
    return decodeLSB_result

def go_decodeAlt(px):
    kontainer = ''
    stop_kontainer = ''
    height,width = np.shape(px)
    index = 0
    row_stop = 0
    stop_status = 0
    for row in range(height):
        for col in range(width):
            if stop_status == 0:
                kontainer = kontainer + str(px[row][col])
                index = index + 1
                print(row," ",col," ", chr(abs(int(kontainer))))
                stop_kontainer = stop_kontainer + chr(abs(int(kontainer)))
                if '~@&' in stop_kontainer:
                    stop_status = 999
                    row_stop = 1
                    print("STOP skuy")
                    break
                else:
                    kontainer = ''
            else:
                row_stop = 1
                break
        if row_stop != 0:
            break
    # print(px)
    decodeLSB_result = stop_kontainer
    return decodeLSB_result
    
def process_decode(stego_img,stego_method,mode):
    if mode == 1:
        stegoImage = cv2.imread(UPLOAD_FOLDER + "/" + stego_img,1)
    else:
        stegoImage = cv2.imread(os.getcwd() + stego_img,1)
    stegoImage = cv2.cvtColor(stegoImage, cv2.COLOR_BGR2RGB)
    
    if stego_method == 'LSB':
        r1, g1, b1 = cv2.split(stegoImage)
        x = 0
        kontainer = ''
        for rgb in range(3):
            if rgb== 0:
                px1 = r1
            elif rgb == 1:
                px1 = g1
            elif rgb == 2:
                px1 = b1

            if '~@&' not in kontainer:
                kontainer = kontainer + go_decodeLSB(px1)
            else:
                print("Log LSB: Stop Decode")
                break
        
        for i in range(len(kontainer)):
            if kontainer[i] == '~' and kontainer[i+1] == '@' and kontainer[i+2] == '&':
                kontainer = kontainer[0:i]
                break

    elif stego_method == 'DCT':
        r1, g1, b1 = cv2.split(stegoImage)
        x,y = np.shape(r1)
        z=0
        i=0
        stop_all = 0
        kontainer = ''
        for rgb in range(3):
            print(rgb)
            if rgb== 0:
                px1 = r1
            elif rgb == 1:
                px1 = g1
            elif rgb == 2:
                px1 = b1
                
            i=0
            while i<(int(x/8))*8:
                j=0
                while j<(int(y/8))*8:
                    px2 = px1[i:i+8,j:j+8]
                    # px2 = np.around(cv2.dct(np.float32(px2)), 1)  
                    px2 = np.around(go_dct(np.float32(px2)), 1)
                    px2 = np.around(px2/quant).astype(int)
                    # newpx = [px2[0][0],px2[0][1],px2[1][0],px2[2][0],px2[1][1],px2[0][2],px2[0][3],px2[1][2]]
                    newpx = [px2[0][3],px2[1][2],px2[2][1],px2[3][0],px2[4][0],px2[3][1],px2[2][2],px2[1][3]]
                    testpx = np.vstack((newpx,px2[1]))
                    if '~@&' not in kontainer:
                        kontainer = kontainer + go_decodeLSB(testpx)
                        kontainer = kontainer[0:-1]
                        z = z + 1
                    else:
                        print("Log DCT: Stop Decode")
                        stop_all = 1
                        break
                    j = j + 8
                if stop_all != 0:
                    break
                else:
                    i = i + 8
            if stop_all != 0:
                break

        for i in range(len(kontainer)):
            if kontainer[i] == '~' and kontainer[i+1] == '@' and kontainer[i+2] == '&':
                kontainer = kontainer[0:i]
                break

    elif stego_method == 'DWT':
        r1, g1, b1 = cv2.split(stegoImage)
        x,y = np.shape(r1)
        z=0
        
        stop_all = 0
        kontainer = ''
        for rgb in range(3):
            if rgb== 0:
                px1 = r1
            elif rgb == 1:
                px1 = g1
            elif rgb == 2:
                px1 = b1
                
            i=0
            while i<(int(x/8))*8:
                j=0
                while j<(int(y/8))*8:
                    px3 = px1[i:i+8,j:j+8]
                    # cA, (cH, cV, cD) = dwt2(px3, 'haar')
                    cA, (cH, cV, cD) = go_dwt(px3)    
                    cH = np.around(cH).astype(int)
                    if '~@&' not in kontainer:
                            kontainer = kontainer + go_decodeLSB(cH)
                            # print(kontainer)
                            z = z + 1
                    else:
                        print("Log DWT: Stop Decode")
                        stop_all = 1
                        break
                    j = j + 8
                if stop_all != 0:
                    break
                else:
                    i = i + 8
            if stop_all != 0:
                break
        for i in range(len(kontainer)):
            if kontainer[i] == '~' and kontainer[i+1] == '@' and kontainer[i+2] == '&':
                kontainer = kontainer[0:i]
                break

    elif stego_method == 'ALL':
        r1, g1, b1 = cv2.split(stegoImage)
        x,y = np.shape(r1)
        z=0
        
        stop_all = 0
        kontainer = ''
        for rgb in range(3):
            if rgb== 0:
                px1 = r1
            elif rgb == 1:
                px1 = g1
            elif rgb == 2:
                px1 = b1
                
            i=0
            while i<(int(x/8))*8:
                j=0
                while j<(int(y/8))*8:
                    px3 = px1[i:i+8,j:j+8]
                    # cA, (cH, cV, cD) = dwt2(px3, 'haar') 
                    cA, (cH, cV, cD) = go_dwt(px3)     
                    # cD = np.round(cv2.dct(np.float32(cD))).astype(int)  
                    cH = np.around(cH).astype(int)
                    if '~@&' not in kontainer:
                            kontainer = kontainer + go_decodeLSB(cH)
                            # print(kontainer)
                            z = z + 1
                    else:
                        print("Log ALL: Stop Decode")
                        stop_all = 1
                        break
                    j = j + 8
                if stop_all != 0:
                    break
                else:
                    i = i + 8
            if stop_all != 0:
                break
        for i in range(len(kontainer)):
            if kontainer[i] == '~' and kontainer[i+1] == '@' and kontainer[i+2] == '&':
                kontainer = kontainer[0:i]
                break

    hidden_obj = kontainer
    return hidden_obj

#=====Route Section=====
@app.route('/')
def index():
    return render_template('hal_home.html')

@app.route('/encode')
def show_encode():
    if os.path.exists(RESULT_FOLDER + encode_folder):
        return render_template('hal_encode.html')
    else:
        os.mkdir(RESULT_FOLDER + encode_folder)
        return render_template('hal_encode.html')

@app.route('/decode')
def show_decode():
    return render_template('hal_decode.html')
    
@app.route('/identify')
def show_identify():
    return render_template('hal_identify.html')

@app.route('/go_encode', methods=['GET', 'POST'])
def go_encode():
    # check if the post request has the file part
    if request.method == 'POST' and 'ori_image' in request.files:
        cover_img = request.files['ori_image']
        if request.form['action'] == 'Encode Pesan' and request.form['hidden_text'] != '' and cover_img.filename != '':
            new_cover_img = go_upload(cover_img,'')
            hidden_text = request.form['hidden_text']
            result_data = process_encode(new_cover_img,hidden_text)
            if result_data != '': 
                return render_template('hal_hasilencode.html', result=result_data)
            else:
                return render_template('hal_error.html')
            
        elif request.form['action'] == 'Encode Gambar' and 'hidden_image' in request.files and cover_img.filename != '':
            hidden_img = request.files['hidden_image']
            new_cover_img = go_upload(cover_img,'')
            new_hidden_img = go_upload(hidden_img,'')
            #img = Image.open(UPLOAD_FOLDER+"/"+hidden_img.filename)
            #proses read dari file
            f = open(UPLOAD_FOLDER+"/"+new_hidden_img, 'rb')
            img = f.read()
            b64 = str(base64.b64encode(img))
            b64 = b64.split("'")
            b64_hidden = 'data:image/png;base64, '+b64[1]
            result_data = process_encode(new_cover_img,b64_hidden)
            if result_data != '':
                # return '<img src="'+b64_hidden+'" />'
                return render_template('hal_hasilencode.html', result=result_data)
            else:
                return render_template('hal_error.html')
        else:
            return render_template('hal_error.html')
    else:
        return render_template('hal_error.html')

@app.route('/go_hitpsnr', methods=['GET', 'POST'])
def go_hitpsnr():
    if request.method == 'POST':
        stego_img1 = request.files['file1']
        stego_img2 = request.files['file2']
        new_stego_img1 = go_upload(stego_img1,1)
        new_stego_img2 = go_upload(stego_img2,2)
        upStego1 = cv2.imread(UPLOAD_FOLDER + "/" + new_stego_img1,1)
        upStego2 = cv2.imread(UPLOAD_FOLDER + "/" + new_stego_img2,1)
        mse,psnr = go_psnr(upStego1,upStego2)
        eucDist = go_eucDist(upStego1,upStego2)
        if psnr != '' and eucDist != '':
            dataPSNR = {
                'mse':mse,
                'psnr':psnr,
                'eucDist' :eucDist
            }
            return dataPSNR
        else:
            return "Tidak Dihitung"

@app.route('/go_decode', methods=['GET', 'POST'])
def go_decode():
    # print(request.files)
    if request.method == 'POST' and request.form['type'] == 'loc':
        print("mlebu sek location")
        stego_loc = request.form['location']
        print(stego_loc)
        stego_method = request.form['method']
        # new_stego_img = go_upload(stego_img)
        hidden_object = process_decode(stego_loc,stego_method,2) 
        if hidden_object != '':
            return hidden_object
        else:
            return "Tidak Ditemukan"
    elif request.method == 'POST' and request.form['type'] == 'file':
        print("mlebu sek file")
        stego_img = request.files['file']
        stego_method = request.form['method']
        print(stego_img)
        makeID = random.randint(1,100)
        new_stego_img = go_upload(stego_img,makeID)
        hidden_object = process_decode(new_stego_img,stego_method,1) 

        if hidden_object != '':
            return hidden_object
        else:
            return "Tidak Ditemukan"
    else:
        return "salah POST"

@app.route('/go_encode/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = RESULT_FOLDER + encode_folder+ "/" + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route('/test')
def testing_page():
    return render_template('hal_hasilencode.html')

if __name__ == "__main__":
    app.run(debug=True)