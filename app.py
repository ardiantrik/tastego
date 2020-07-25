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

def process_encode(cover_img, hidden_text):
    global coverImage, hiddenObject, r1, g1, b1, r2, b2, g2

    # #LSB tok
    # #=================Library Stegano===========
    # secret = lsb.hide(UPLOAD_FOLDER + "/" + cover_img, hidden_text)
    # secret.save(UPLOAD_FOLDER + "/" + encode_folder + "/LSB-" + cover_img)
    
    #=================TEST=======================
    #  width, height = img.size
    #     index = 0
    #     for row in range(height):
    #         for col in range(width):
    #             if img.mode != 'RGB':
    #                 #r, g, b ,a = img.getpixel((col, row))
    #                 img = img.convert("RGB")
    #                 r, g, b = img.getpixel((col, row))
    #                 print ("r:"+str(r)+"_g:"+str(g)+"_b:"+str(b))
    #             elif img.mode == 'RGB':
    #                 r, g, b = img.getpixel((col, row))
    #                 print ("r:"+str(r)+"_g:"+str(g)+"_b:"+str(b))
    #             # first value is length of msg
    #             if row == 0 and col == 0 and index < length:
    #                 asc = length
    #             elif index <= length:
    #                 c = msg[index -1]
    #                 asc = ord(c)
    #             else:
    #                 asc = b
    #             encoded.putpixel((col, row), (r, g , asc))
    #             index += 1
    #     return encoded

    #DCT
    # =====Wes jalan tp rung dadi====
    coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    r1, g1, b1 = cv2.split(coverImage)
    
    # r3 = dct(r1)
    # g3 = dct(g1)
    # b3 = dct(b1)

    r1 = cv2.dct(np.float32(r1))
    g1 = cv2.dct(np.float32(g1))
    b1 = cv2.dct(np.float32(b1))
    
    # print("=====hasil DCT=====")
    r1 = np.round(r1).astype(int)
    g1 = np.round(g1).astype(int)
    b1 = np.round(b1).astype(int)

    img = cv2.merge((b1,g1,r1))
    cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/DCT-" + cover_img, img) 

    coverImage = cv2.imread(UPLOAD_FOLDER + "/"+ encode_folder +"/DCT-" + cover_img,1)
    coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    r2, g2, b2 = cv2.split(coverImage)

    r2 = cv2.idct(np.float32(r1))
    g2 = cv2.idct(np.float32(g1))
    b2 = cv2.idct(np.float32(b1))

    # print("===Hasil IDCT====")
    r2 = np.round(r2).astype(int)
    g2 = np.round(g2).astype(int)
    b2 = np.round(b2).astype(int)

    img = cv2.merge((b2,g2,r2))
    cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/IDCT-" + cover_img, img) 


    # #DWT
    # coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    # # print(coverImage)
    # cA, (cH, cV, cD) = dwt2(coverImage, 'haar')  
    # coeffs = cA, (cH, cV, cD)
    # # iki le nyematke LSB py ?
    # # print(coeffs)
    # img = idwt2(coeffs, 'haar')
    # print("===Hasil DWT====")
    # print(np.uint8(img))
    # b1 = img[:, :, 0]
    # g1 = img[:, :, 1]
    # r1 = img[:, :, 2]
    # img = cv2.merge((b1,g1,r1))
    # print("=====")
    # print(np.uint8(img))
    # cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/DWT-" + cover_img, img)
    return 'success'

def process_decode(stego_img):
    hidden_obj= lsb.reveal(UPLOAD_FOLDER + "/" +stego_img)
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
                return 'iso'
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
            b64_hidden = 'data:image;base64, '+b64[1]
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
        new_stego_img = go_upload(stego_img)
        hidden_object = process_decode(new_stego_img) 
        if hidden_object != '':
            return hidden_object
        else:
            return "salah decode"
    else:
        return "salah POST"

@app.route('/go_encode/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(debug=True)