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
# from stegano import lsb
# from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2
import math

encode_folder = "Encoded_image_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M"))
decode_folder= "Decoded_image_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M"))
UPLOAD_FOLDER = os.getcwd() + '/assets/'
RESULT_FOLDER = os.getcwd() + '/static/result/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','bmp', 'tif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

#=====Method Section=====
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def go_upload(file_up):
    if file_up and allowed_file(file_up.filename):
        filename = secure_filename(file_up.filename)
        file_up.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return filename

def go_psnr(cover_img,stego_img):
    dimensiCover = np.shape(cover_img)
    dimensiStego = np.shape(stego_img)
    print(dimensiCover[0]*dimensiCover[1])
    # [0] = height, [1] = width, [2] = color channel
    if (dimensiCover[0]*dimensiCover[1]) != (dimensiStego[0]*dimensiStego[1]):
        mse = (dimensiCover[0]*dimensiCover[1])-(dimensiStego[0]*dimensiStego[1])
        # psnr = "Beda Dimensi"
    else:
        mse = np.mean((cover_img - stego_img) ** 2 )
        
    if mse == 0:
        psnr = 100
    else:
        PIXEL_MAX = 255.0
        psnr = 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    
    return mse,psnr

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
    # print(px)
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
    global coverImage, r1, g1, b1, r2, b2, g2

    coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    cover = coverImage
    coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    # cover = coverImage
    hid = hidden_text+'~@&'
    hit_hidden = len(hid)
    print(hid)
    kontainer = ''
    kontainer2 = ''
    kontainer3 = ''
    kontainer_div = [['']]
    kontainer_div2 = [['']]
    kontainer_div3 = [['']]

    x = 0
    y = 0
    for i in range(hit_hidden):
        # print(i, " " , hid[i])
        kontainer = kontainer + f'{ord(hid[i]):08b}'
        kontainer2 = kontainer2 + f'{ord(hid[i]):08b}'
        # kontainer2 = kontainer2 + hid[i]
        kontainer3 = kontainer3 + f'{ord(hid[i]):08b}'
        if (i+1)%8 == 0:
            if x == 0:
                kontainer_div2[x] = kontainer2
            else:
                kontainer_div2.append(kontainer2)
            kontainer2 = ''
            x = x + 1
        
        # # NGGO DCT ALT ENCODE
        # if (i+1)%64 == 0:
        #     if x == 0:
        #         kontainer_div2[x] = kontainer2
        #     else:
        #         kontainer_div2.append(kontainer2)
        #     kontainer2 = ''
        #     x = x + 1

        if (i+1)%2 == 0:
            if y == 0:
                kontainer_div3[y] = kontainer3
            else:
                kontainer_div3.append(kontainer3)
            kontainer3 = ''
            y = y + 1
    # print(kontainer2)
    if kontainer2 != '' and kontainer_div2 == [['']]:
        kontainer_div2[0] = kontainer2
    elif kontainer2!= '':
        kontainer_div2.append(kontainer2)
    if kontainer3 != '':
        kontainer_div3.append(kontainer3)
    print(kontainer_div2)
    # print(len(kontainer_div2))

    # print(kontainer_div)
    # print(len(kontainer_div))

    r1, g1, b1 = cv2.split(coverImage)
    
    #LSB tok
    r1, g1, b1 = cv2.split(coverImage)
    p,l = np.shape(r1)
    x = 0
    kont = ''
    if len(kontainer)>(p*l):
        for i in range(len(kontainer)):
            kont = kont + kontainer[i]
            if (i+1)%(p*l) == 0:
                if x == 0:
                    kontainer_div[x] = kont
                else:
                    kontainer_div.append(kont)
                kont = ''
                x = x + 1
                print(x)
        
        if kont != '':
            kontainer_div.append(kont)
        # print(kontainer_div)
            # if i == 0:
            #     kontainer_div[x] = kontainer[i]
            # elif i == (p*l):
            #     kontainer_div[x] = kontainer[i]
            #     x = x + 1
            #     print("here")
            # else:
            #     kontainer_div[x] = kontainer_div[x] + kontainer[i]
            #     # kontainer_div.append(kontainer)
            #     # print(kontainer_div)
    else:
        kontainer_div[x] = kontainer
    # print(kontainer_div)
    x = 0
    for i in range(3):
        if i== 0:
            px1 = r1
        elif i == 1:
            px1 = g1
        elif i == 2:
            px1 = b1

        if x<len(kontainer_div):
            px1 = go_encodeLSB(px1,kontainer_div[i])

            if i== 0:
                r1 = px1
            elif i == 1:
                g1 = px1
            elif i == 2:
                b1 = px1

            x = x + 1
        else:
            break
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
    # bermasalah nang encode karena diround(pembulatan)
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
                px2 = px1[i:i+8,j:j+8]

                # px2 = np.uint8(cv2.dct(np.float32(px2)))
                px2 = np.around(cv2.dct(np.float32(px2))).astype(int)

                if z<len(kontainer_div2):
                    # print(z, " ", kontainer_div2[z])
                    px2 = go_encodeLSB(px2,kontainer_div2[z])
                    # print(kontainer_div2[z])
                    # px2 = go_encodeAlt(px2,kontainer_div2[z])
                    

                    # px2 = np.uint8(cv2.idct(np.float32(px2)))
                    # px2 = np.around(cv2.idct(np.float32(px2))).astype(int)

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
                px3 = px1[i:i+8,j:j+8]
                # print(px3)
                cA, (cH, cV, cD) = dwt2(px3, 'haar')  
                cH = np.around(cH).astype(int)
                if z<len(kontainer_div3):
                    # print(z, " ", kontainer_div3[z])
                    cH = go_encodeLSB(cH,kontainer_div3[z])
                    px3 = cA.astype(int),(cH.astype(int), cV.astype(int), cD.astype(int))
                    px3 = idwt2(px3, 'haar')
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
                px3 = px1[i:i+8,j:j+8]
                # print(px3)
                cA, (cH, cV, cD) = dwt2(px3, 'haar')  
                cD = np.round(cv2.dct(np.float32(cD))).astype(int)
                cD = np.around(cD).astype(int)
                if z<len(kontainer_div3):
                    # print(z, " ", kontainer_div3[z])
                    cD = go_encodeLSB(cD,kontainer_div3[z])
                    # cD = np.round(cv2.idct(np.float32(cD))).astype(int)
                    px3 = cA.astype(int),(cH.astype(int), cV.astype(int), cD.astype(int))
                    px3 = idwt2(px3, 'haar')
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
    # result_data =[dataLSB, dataDCT]
    # print(result_data)
    return result_data

def go_decodeLSB(px):
    kontainer = ''
    stop_kontainer = ''
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
    #LSB
    # ======Iki kendalane ana nang pembatas=======
    # hidden_obj= lsb.reveal(UPLOAD_FOLDER + "/" +stego_img)
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
                break

        for i in range(len(kontainer)):
            if kontainer[i] == '~' and kontainer[i+1] == '@' and kontainer[i+2] == '&':
                kontainer = kontainer[0:i]
                break

    elif stego_method == 'DCT':
        # print("================DEKODE===============")
        r1, g1, b1 = cv2.split(stegoImage)
        x,y = np.shape(r1)
        z=0
        i=0
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
                    px2 = px1[i:i+8,j:j+8]
                    # px2 = np.uint8(cv2.dct(np.float32(px2)))
                    # px2 = np.around(cv2.dct(np.float32(px2))).astype(int)  
                    if '~@&' not in kontainer:
                            kontainer = kontainer + go_decodeLSB(px2)
                            # kontainer = kontainer + go_decodeAlt(px2)
                            # print(kontainer)
                            z = z + 1
                    else:
                        print("DCTtekan kene ra sih?")
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
        # print("================DEKODE===============")
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
                    cA, (cH, cV, cD) = dwt2(px3, 'haar')   
                    cH = np.around(cH).astype(int)
                    if '~@&' not in kontainer:
                            kontainer = kontainer + go_decodeLSB(cH)
                            # print(kontainer)
                            z = z + 1
                    else:
                        print("DWTtekan kene ra sih?")
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
        # print("================DEKODE===============")
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
                    cA, (cH, cV, cD) = dwt2(px3, 'haar')   
                    # cD = np.round(cv2.dct(np.float32(cD))).astype(int)  
                    cD = np.around(cD).astype(int)
                    if '~@&' not in kontainer:
                            kontainer = kontainer + go_decodeLSB(cD)
                            # print(kontainer)
                            z = z + 1
                    else:
                        print("ALLtekan kene ra sih?")
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

    # print(kontainer)
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
            new_cover_img = go_upload(cover_img)
            hidden_text = request.form['hidden_text']
            result_data = process_encode(new_cover_img,hidden_text)
            if result_data != '': 
                return render_template('hal_hasilencode.html', result=result_data)
            else:
                return render_template('hal_error.html')
            
        elif request.form['action'] == 'Encode Gambar' and 'hidden_image' in request.files and cover_img.filename != '':
            hidden_img = request.files['hidden_image']
            new_cover_img = go_upload(cover_img)
            new_hidden_img = go_upload(hidden_img)
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
        new_stego_img1 = go_upload(stego_img1)
        new_stego_img2 = go_upload(stego_img2)
        upStego1 = cv2.imread(UPLOAD_FOLDER + "/" + new_stego_img1,1)
        upStego2 = cv2.imread(UPLOAD_FOLDER + "/" + new_stego_img2,1)
        mse,psnr = go_psnr(upStego1,upStego2)
        if psnr != '':
            dataPSNR = {
                'mse':mse,
                'psnr':psnr
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
        print(stego_method)
        new_stego_img = go_upload(stego_img)
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