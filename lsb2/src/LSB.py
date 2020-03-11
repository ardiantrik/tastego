import os
import xlwt
import shutil
import cv2
import sys
import math
import numpy as np
import itertools
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
#from scipy import signal
quant = np.array([[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE
                    [12,12,14,19,26,58,60,55],    # required for DCT
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])


class LSB():
    #encoding part :
    def encode_image(self,img, msg):
        length = len(msg)
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        encoded = img.copy()
        width, height = img.size
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index -1]
                    asc = ord(c)
                else:
                    asc = b
                encoded.putpixel((col, row), (r, g , asc))
                index += 1
        return encoded

    #decoding part :
    def decode_image(self,img):
        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))  
                # first pixel r value is length of message
                if row == 0 and col == 0:
                    length = b
                elif index <= length:
                    msg += chr(b)
                index += 1
        lsb_decoded_image_file = "lsb_" + original_image_file
        #img.save(lsb_decoded_image_file)
        ##print("Decoded image was saved!")
        return msg

class Compare():
    def correlation(self, img1, img2):
        return signal.correlate2d (img1, img2)
    def meanSquareError(self, img1, img2):
        error = np.sum((img1.astype('float') - img2.astype('float')) ** 2)
        error /= float(img1.shape[0] * img1.shape[1]);
        return error
    def psnr(self, img1, img2):
        mse = self.meanSquareError(img1,img2)
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))



#driver part :
#deleting previous folders :
if os.path.exists("Encoded_image/"):
    shutil.rmtree("Encoded_image/")
if os.path.exists("Decoded_output/"):
    shutil.rmtree("Decoded_output/")
if os.path.exists("Comparison_result/"):
    shutil.rmtree("Comparison_result/")
#creating new folders :
os.makedirs("Encoded_image/")
os.makedirs("Decoded_output/")
os.makedirs("Comparison_result/")
original_image_file = ""    # to make the file name global variable
lsb_encoded_image_file = ""


while True:
    m = input("To encode press '1', to decode press '2', to compare press '3', press any other button to close: ")

    if m == "1":
        os.chdir("Original_image/")
        original_image_file = input("Enter the name of the file with extension : ")
        lsb_img = Image.open(original_image_file)
        print("Description : ",lsb_img,"\nMode : ", lsb_img.mode)
        secret_msg = input("Enter the message you want to hide: ")
        print("The message length is: ",len(secret_msg))
        os.chdir("..")
        os.chdir("Encoded_image/")
        lsb_img_encoded = LSB().encode_image(lsb_img, secret_msg)
        lsb_encoded_image_file = "lsb_" + original_image_file
        lsb_img_encoded.save(lsb_encoded_image_file)
        print("Encoded images were saved!")
        os.chdir("..")

    elif m == "2":
        os.chdir("Encoded_image/")
        lsb_img = Image.open(lsb_encoded_image_file)
        os.chdir("..") #going back to parent directory
        os.chdir("Decoded_output/")
        lsb_hidden_text = LSB().decode_image(lsb_img)
        file = open("lsb_hidden_text.txt","w")
        file.write(lsb_hidden_text) # saving hidden text as text file
        file.close()
        print("Hidden texts were saved as text file!")
        os.chdir("..")
    elif m == "3":
        #comparison calls
        os.chdir("Original_image/")
        original = cv2.imread(original_image_file)
        os.chdir("..")
        os.chdir("Encoded_image/")
        lsbEncoded = cv2.imread(lsb_encoded_image_file)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        lsb_encoded_img = cv2.cvtColor(lsbEncoded, cv2.COLOR_BGR2RGB)
        os.chdir("..")
        os.chdir("Comparison_result/")

        book = xlwt.Workbook()
        sheet1=book.add_sheet("Sheet 1")
        style_string = "font: bold on , color red; borders: bottom dashed"
        style = xlwt.easyxf(style_string)
        sheet1.write(0, 0, "Original vs", style=style)
        sheet1.write(0, 1, "MSE", style=style)
        sheet1.write(0, 2, "PSNR", style=style)
        sheet1.write(1, 0, "LSB")
        sheet1.write(1, 1, Compare().meanSquareError(original, lsb_encoded_img))
        sheet1.write(1, 2, Compare().psnr(original, lsb_encoded_img))
        book.save("Comparison.xls")
        print("Comparison Results were saved as xls file!")
        os.chdir("..")
    else:
        print("Closed!")
        break