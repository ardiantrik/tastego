import os
import base64
import cv2
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
from datetime import datetime

encode_folder = "Encoded_image_" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
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
    
    return 'success'
    

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

# @app.route('/image2matrix', methods=['POST'])
# def image2matrix():
#     return "haha"

@app.route('/go_encode', methods=['GET', 'POST'])
def go_encode():
    # check if the post request has the file part
    if request.method == 'POST' and 'ori_image' in request.files:
        cover_img = request.files['ori_image']
        if request.form['action'] == 'Encode Pesan' and request.form['hidden_text'] != '' and cover_img.filename != '':
            go_upload(cover_img)
            hidden_text = request.form['hidden_text']
            return hidden_text
        elif request.form['action'] == 'Encode Gambar' and 'hidden_image' in request.files and cover_img.filename != '':
            hidden_img = request.files['hidden_image']
            go_upload(cover_img)
            go_upload(hidden_img)
            
        else:
            return render_template('hal_error.html')
    else:
        return render_template('hal_error.html')

@app.route('/go_encode/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(debug=True)