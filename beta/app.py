import os
import base64
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime
from stegano import lsb

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

    #LSB tok
    #secret = lsb.hide(UPLOAD_FOLDER + "/" + cover_img, hidden_text)
    #secret.save(UPLOAD_FOLDER + "/" + encode_folder + "/LSB-" + cover_img)

    #DCT
    coverImage = cv2.imread(UPLOAD_FOLDER + "/" + cover_img,1)
    coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    r1 = coverImage[:, :, 0]
    g1 = coverImage[:, :, 1]
    b1 = coverImage[:, :, 2]

    rf32 = np.float32(r1) 
    gf32 = np.float32(g1)
    bf32 = np.float32(b1)

    r2 = cv2.dct(rf32)
    g2 = cv2.dct(gf32)
    b2 = cv2.dct(bf32)

    r1 = np.uint8(r2)
    g1 = np.uint8(g2)
    b1 = np.uint8(b2)


    #coverImages = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    print(r1)
    img = cv2.merge((b1,g1,r1))
    print(UPLOAD_FOLDER + "/"+ encode_folder +"/DCT_" + cover_img)
    cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/DCT_" + cover_img, img) 

    coverImage = cv2.imread(UPLOAD_FOLDER + "/"+ encode_folder +"/DCT_" + cover_img,1)
    coverImage = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    r1 = coverImage[:, :, 0]
    g1 = coverImage[:, :, 1]
    b1 = coverImage[:, :, 2]

    rf32 = np.float32(r1)
    gf32 = np.float32(g1)
    bf32 = np.float32(b1)

    r2 = cv2.idct(rf32)
    g2 = cv2.idct(gf32)
    b2 = cv2.idct(bf32)

    r1 = np.uint8(r2)
    g1 = np.uint8(g2)
    b1 = np.uint8(b2)


    #coverImages = cv2.cvtColor(coverImage, cv2.COLOR_BGR2RGB)
    print(r1)
    img = cv2.merge((b1,g1,r1))
    cek = cv2.imwrite(UPLOAD_FOLDER + encode_folder +"/IDCT_" + cover_img, img) 
    #coverImage = cv2.resize(coverImage,(400,400))

    #DWT

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