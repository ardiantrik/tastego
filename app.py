import os
import base64
import cv2
import numpy as np
import PIL  
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime
from stegano import lsb
from scipy.fftpack import dct, idct
from pywt import dwt2, idwt2

encode_folder = "Encoded_image_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
decode_folder= "Decoded_image_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
UPLOAD_FOLDER = os.getcwd() + '/assets/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#=====Method Section=====
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def go_upload(file_up):
    if file_up and allowed_file(file_up.filename):
        filename = secure_filename(file_up.filename)
        file_up.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return filename

def go_encodeLSB(r1,g1,b1,kontainer):
    hit_kontainer = len(kontainer)
    height,width = np.shape(r1)
    index = 0
    status_rgb = 0
    row = 0
    row_reset = 0
    row_stop = 0
    # for row in range(height):
    #     for col in range(width):
    while row<height:
        col = 0
        col_reset = 0
        while col<width:
            if index<hit_kontainer:
                if status_rgb == 0:
                    bit_temp = f'{r1[row][col]:08b}'
                    bit_lsb = list(bit_temp)
                    bit_lsb[-1] = kontainer[index]
                    bit_temp = ''.join(bit_lsb)
                    r1[row][col] = int(bit_temp,2)
                elif status_rgb == 1:
                    bit_temp = f'{g1[row][col]:08b}'
                    bit_lsb = list(bit_temp)
                    bit_lsb[-1] = kontainer[index]
                    bit_temp = ''.join(bit_lsb)
                    g1[row][col] = int(bit_temp,2)
                elif status_rgb == 2:
                    bit_temp = f'{b1[row][col]:08b}'
                    bit_lsb = list(bit_temp)
                    bit_lsb[-1] = kontainer[index]
                    bit_temp = ''.join(bit_lsb)
                    b1[row][col] = int(bit_temp,2)
                index = index + 1
                # if index>height*width and index<hit_kontainer and status == 0:
            elif index<hit_kontainer and row == height and col == width:
                status_rgb = status_rgb + 1
                row_reset=1
                col_reset=1
                print("reset status" + str(status_rgb))
            else:
                row_stop = 1
                break
            
            if col_reset == 0:
                col = col + 1
                # print(col, 'iki col tambah')
            else:
                col = 0
                col_reset=0

        if row_stop != 0:
            break

        if row_reset == 0:
            row = row + 1
            # print(row, 'iki row tambah')
        else:
            row = 0
            row_reset=0
        
    
    return r1,g1,b1

def process_encode(cover_img, hidden_text):
    global coverImage, r1, g1, b1, r2, b2, g2

    coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    hid = hidden_text+'~@&'
    hit_hidden = len(hid)
    print(hit_hidden)
    kontainer = ''
    kontainer2 = ''
    kontainer_div = ['']
    x = 0
    for i in range(hit_hidden):
        kontainer = kontainer + f'{ord(hid[i]):08b}'
        kontainer2 = kontainer2 + f'{ord(hid[i]):08b}'
        if (i+1)%8 == 0:
            if x == 0:
                kontainer_div[x] = kontainer2
            else:
                kontainer_div.append(kontainer2)
            kontainer2 = ''
            x = x + 1
    if kontainer2 != '':
        kontainer_div.append(kontainer2)
    print(kontainer_div)
    print(len(kontainer_div))

    r1, g1, b1 = cv2.split(coverImage)
    
    #LSB tok
    r1, g1, b1 = go_encodeLSB(r1,g1,b1,kontainer)
    img = cv2.merge((b1,g1,r1))
    cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/LSB-" + cover_img, img)

    #DCT
    # bermasalah nang encode karena luwih seko 255
    # print(len(kontainer_div))
    # print(r1)
    x,y = np.shape(r1)
    z=0
    i=0
    while i<(int(x/8))*8:
        j=0
        while j<(int(y/8))*8:
            r3 = r1[i:i+8,j:j+8]
            g3 = g1[i:i+8,j:j+8]
            b3 = b1[i:i+8,j:j+8]
            
            r3 = np.round(cv2.dct(np.float32(r3))).astype(int)
            g3 = np.round(cv2.dct(np.float32(g3))).astype(int)
            b3 = np.round(cv2.dct(np.float32(b3))).astype(int)

            if z<len(kontainer_div):
                print(z)
                print(kontainer_div[z])
                r3, g3, b3 = go_encodeLSB(r3,g3,b3,kontainer_div[z])
                z = z + 1
            else:
                break

            # r3 = np.round(cv2.idct(np.float32(r3))).astype(int)
            # g3 = np.round(cv2.idct(np.float32(g3))).astype(int)
            # b3 = np.round(cv2.idct(np.float32(b3))).astype(int)

            r1[i:i+8,j:j+8] = r3
            g1[i:i+8,j:j+8] = g3
            b1[i:i+8,j:j+8] = b3

            j = j + 8
        i = i + 8

    img = cv2.merge((b1,g1,r1))
    cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/DCT-" + cover_img, img)

            


    


    # #DCT
    # # =====Wes jalan tp rung dadi====
    # coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    # coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    # r1, g1, b1 = cv2.split(coverImage)

    # r1 = cv2.dct(np.float32(r1))
    # g1 = cv2.dct(np.float32(g1))
    # b1 = cv2.dct(np.float32(b1))
    
    # # print("=====hasil DCT=====")
    # r1 = np.round(r1).astype(int)
    # g1 = np.round(g1).astype(int)
    # b1 = np.round(b1).astype(int)

    # # img = cv2.merge((b1,g1,r1))
    # # cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/DCT-" + cover_img, img) 

    # # coverImage = cv2.imread(UPLOAD_FOLDER + "/"+ encode_folder +"/DCT-" + cover_img,1)
    # # coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    # # r2, g2, b2 = cv2.split(coverImage)

    # # TO DO : iki le nyematke LSB py?

    # r2 = cv2.idct(np.float32(r1))
    # g2 = cv2.idct(np.float32(g1))
    # b2 = cv2.idct(np.float32(b1))

    # # print("===Hasil IDCT====")
    # r2 = np.round(r2).astype(int)
    # g2 = np.round(g2).astype(int)
    # b2 = np.round(b2).astype(int)

    # img = cv2.merge((b2,g2,r2))
    # cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/DCT-" + cover_img, img) 


    #DWT
    # coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    # # print(coverImage)
    # coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    # r1, g1, b1 = cv2.split(coverImage)
    
    # rcA, (rcH, rcV, rcD) = dwt2(r1, 'haar')  
    # r1_coeffs = rcA.astype(int),(rcH.astype(int), rcV.astype(int), rcD.astype(int))
    # gcA, (gcH, gcV, gcD) = dwt2(g1, 'haar')  
    # g1_coeffs = gcA.astype(int),(gcH.astype(int), gcV.astype(int), gcD.astype(int))
    # bcA, (bcH, bcV, bcD) = dwt2(b1, 'haar')  
    # b1_coeffs = bcA.astype(int),(bcH.astype(int), bcV.astype(int), bcD.astype(int))
    # # print(len(rcD))
    # # TO DO : iki le nyematke LSB py ?
    # klmt = hidden_text
    # print(klmt)
    # x,y = np.shape(bcD)
    # print(x)
    # print(y)
    # z=0
    # for i in range(x):
    #     for j in range(y):
    #         if i==0 and j==0:
    #             bcD[i][j] = len(klmt)
    #             print(len(klmt))
    #         else:
    #             if z<len(klmt):
    #                 bcD[i][j] = ord(klmt[z])
    #                 z = z+1
    #             else:
    #                 break
    
    # b1_coeffs = bcA.astype(int),(bcH.astype(int), bcV.astype(int), bcD.astype(int))
    # # print(coeffs)
    # # img = idwt2(coeffs, 'haar')
    # full_r = idwt2(r1_coeffs, 'haar')
    # full_g = idwt2(g1_coeffs, 'haar')
    # full_b = idwt2(b1_coeffs, 'haar')
    # # print(full_r)
    # # print("===Hasil DWT====")
    # # print(np.uint8(img))
    # bcA, (bcH, bcV, bcD) = dwt2(full_b, 'haar')  
    # z=0
    # kontainer = ''
    # x,y = np.shape(bcD)
    # for i in range(x):
    #     for j in range(y):
    #         if i == 0 and j == 0:
    #             jumlah = np.round(bcD[i][j]).astype(int)
    #             print(jumlah)
    #         else:
    #             if z<abs(jumlah):
    #                 kontainer = kontainer + chr(np.round(bcD[i][j]).astype(int))
    #                 z = z+1
    #                 print(chr(np.round(bcD[i][j]).astype(int)))
    #             else:
    #                 break
    # print(kontainer)
    
    # # b3 = img[:, :, 0]
    # # g3 = img[:, :, 1]
    # # r3 = img[:, :, 2]
    # img = cv2.merge((full_b.astype(int),full_g.astype(int),full_r.astype(int)))
    # # print(img)
    # print("=====")
    # # print(np.uint8(img))
    # cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/DWT-" + cover_img, img)
    return 'success'

def go_decodeLSB(r1,g1,b1):
    
    height,width = np.shape(r1)
    kontainer = ''
    # x = 1
    index = 0
    status_rgb = 0
    stop_check = ''
    stop_kontainer = ''
    stop_status = 0
    row = 0
    row_reset = 0
    row_stop = 0
    # for row in range(height):
        # for col in range(width):
    while row<height:
        col = 0
        col_reset = 0
        while col<width:
            if stop_status == 0 and status_rgb < 3:
                if status_rgb == 0:
                    bit_temp = f'{r1[row][col]:08b}'
                    kontainer = kontainer + bit_temp[-1]
                    stop_check = stop_check + bit_temp[-1]
                elif status_rgb == 1:
                    bit_temp = f'{g1[row][col]:08b}'
                    kontainer = kontainer + bit_temp[-1]
                    stop_check = stop_check + bit_temp[-1]
                elif status_rgb == 2:
                    bit_temp = f'{b1[row][col]:08b}'
                    kontainer = kontainer + bit_temp[-1]
                    stop_check = stop_check + bit_temp[-1]
                index = index + 1

                if index%8 == 0:
                    stop_kontainer = stop_kontainer + chr(int(stop_check,2))
                    if '~@&' in stop_kontainer:
                        stop_status = 999
                        print("STOP skuy")
                        break
                    else:
                        stop_check = ''
                # x = x + 1
            elif row == height and col == width:
                status_rgb = status_rgb + 1
                row_reset=1
                col_reset=1
                print("reset status" + str(status_rgb))
            else:
                row_stop = 1
                print(row, " dan ", col, "STOP KABEH")
                break

            if col_reset == 0:
                col = col + 1
            else:
                col = 0
                col_reset=0

        if row_stop != 0:
            break

        if row_reset == 0:
            row = row + 1
        else:
            row = 0
            row_reset=0

    kontainer = stop_kontainer
    if height !=8 and width !=8:
        for i in range(len(kontainer)):
            if kontainer[i] == '~' and kontainer[i+1] == '@' and kontainer[i+2] == '&':
                kontainer = kontainer[0:i]
                break
    
    decodeLSB_result = kontainer
    return decodeLSB_result
    
def process_decode(stego_img,stego_method):
    #LSB
    # ======Iki kendalane ana nang pembatas=======
    # hidden_obj= lsb.reveal(UPLOAD_FOLDER + "/" +stego_img)
    stegoImage = cv2.imread(UPLOAD_FOLDER + "/" + stego_img,1)
    stegoImage = cv2.cvtColor(stegoImage, cv2.COLOR_BGR2RGB)
    r1, g1, b1 = cv2.split(stegoImage)
    
    if stego_method == 'LSB':
        kontainer = go_decodeLSB(r1,g1,b1)
    elif stego_method == 'DCT':
        # print("================DEKODE===============")
        x,y = np.shape(r1)
        z=0
        i=0
        stop_x = 0
        kontainer = ''
        while i<(int(x/8))*8:
            j=0
            while j<(int(y/8))*8:
                r3 = r1[i:i+8,j:j+8]
                g3 = g1[i:i+8,j:j+8]
                b3 = b1[i:i+8,j:j+8]
                
                # r3 = np.round(cv2.dct(np.float32(r3))).astype(int)
                # g3 = np.round(cv2.dct(np.float32(g3))).astype(int)
                # b3 = np.round(cv2.dct(np.float32(b3))).astype(int)

                if '~@&' not in kontainer:
                    kontainer = kontainer + go_decodeLSB(r3,g3,b3)
                    z = z + 1
                else:
                    print(kontainer)
                    for i in range(len(kontainer)):
                        if kontainer[i] == '~' and kontainer[i+1] == '@' and kontainer[i+2] == '&':
                            kontainer = kontainer[0:i]
                            break
                    print("tekan kene ra sih?")
                    stop_x = 1
                    break
                j = j + 8

            if stop_x != 0:
                break
            else:
                i = i + 8

    elif stego_method == 'DWT':
        kontainer = 'rung gawe DWT'
        # hidden_object = process_decodeDWT(new_stego_img)
    elif stego_method == 'ALL':
        kontainer = 'rung gawe Kombinasi LSB+DCT+DWT'
        # hidden_object = process_decodeALL(new_stego_img)

    #DCT

    # DWT
    # ======Iki kendalane ana nang ganti nek nang dekomposisi=======
    # stegoImage = cv2.imread(UPLOAD_FOLDER + "/" + stego_img,1)
    # stegoImage = cv2.cvtColor(stegoImage, cv2.COLOR_BGR2RGB)
    # r1, g1, b1 = cv2.split(stegoImage)

    # bcA, (bcH, bcV, bcD) = dwt2(b1, 'haar')  
    # # b1_coeffs = bcA.astype(int),(bcH.astype(int), bcV.astype(int), bcD.astype(int))

    # z=0
    # kontainer = ''
    # x,y = np.shape(bcD)
    # for i in range(x):
    #     for j in range(y):
    #         if i == 0 and j == 0:
    #             jumlah = np.round(bcD[i][j]).astype(int)
    #             print(jumlah)
    #         else:
    #             if z<abs(jumlah):
    #                 kontainer = kontainer + chr(np.round(bcD[i][j]).astype(int))
    #                 z = z+1
    #                 print(chr(np.round(bcD[i][j]).astype(int)) + ' or '+ str(np.round(bcD[i][j]).astype(int)) + ' from ' + str(bcD[i][j]))
    #             else:
    #                 break
    # print(kontainer)
    hidden_obj = kontainer
    return hidden_obj

#=====Route Section=====
@app.route('/')
def index():
    return render_template('hal_home.html')

@app.route('/encode')
def show_encode():
    if os.path.exists(UPLOAD_FOLDER + encode_folder):
        return render_template('hal_encode.html')
    else:
        os.mkdir(UPLOAD_FOLDER + encode_folder)
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
            if process_encode(new_cover_img,hidden_text) == 'success':
                return render_template('hal_home.html')
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
            if process_encode(new_cover_img,b64_hidden) == 'success':
                return '<img src="'+b64_hidden+'" />'
            else:
                return render_template('hal_error.html')

            
        else:
            return render_template('hal_error.html')
    else:
        return render_template('hal_error.html')

@app.route('/go_decode', methods=['GET', 'POST'])
def go_decode():
    if request.method == 'POST':
        stego_img = request.files['file']
        stego_method = request.form['method']
        print(stego_method)
        new_stego_img = go_upload(stego_img)
        hidden_object = process_decode(new_stego_img,stego_method) 

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

if __name__ == "__main__":
    app.run(debug=True)