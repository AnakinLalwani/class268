import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    operation_selection = request.form['image_type']
    image_file = request.files['file']
    filename = secure_filename(image_file.filename)
    reading_file_data = image_file.read()
    image_array = np.fromstring(reading_file_data, dtype='uint8')
    decode_array_to_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)


    # Write code for Select option for Gray and Sketch
    if operation_selection == "gray":
        file_data = make_grayscale(decode_array_to_img)
    elif operation_selection == "sketch":
        file_data = image_sketch(decode_array_to_img)
    elif operation_selection == "oil":
        file_data = oil_paint(decode_array_to_img)
    elif operation_selection == "rgb":
        file_data = rgb_image(decode_array_to_img)
    elif operation_selection == "water":
        file_data = water_color_effect(decode_array_to_img)
    elif operation_selection == "invert":
        file_data = inverted_effect(decode_array_to_img)
    elif operation_selection == "HDR":
        file_data = hdr_image(decode_array_to_img)
    else:
        print("No image type given.")
    # Ends here

    with open(os.path.join('static/', filename),
                  'wb') as f:
        f.write(file_data)

    return render_template('upload.html', filename=filename)

def make_grayscale(decode_array_to_img):

    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img)

    return output_image


# Write code for Sketch function
def image_sketch(decode_array_to_img):
    gray_image = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    sharpen_gray = cv2.bitwise_not(gray_image)
    blur_sharpened = cv2.GaussianBlur(sharpen_gray, (111, 111), 0)
    sharpen_blur = cv2.bitwise_not(blur_sharpened)
    sketched_image = cv2.divide(gray_image, sharpen_blur, scale = 256.0)

    stautus, output_image = cv2.imencode('.PNG', sketched_image)
    return output_image
# Ends here

def oil_paint(decode_array_to_img):

    converted_oil_img = cv2.xphoto.oilPainting(decode_array_to_img, 7, 1)
    status, output_image = cv2.imencode('.PNG', converted_oil_img)

    return output_image

def rgb_image(decode_array_to_img):

    converted_rgb_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_BGR2RGB)
    status, output_image = cv2.imencode('.PNG', converted_rgb_img)

    return output_image

def water_color_effect(decode_array_to_img):

    converted_water_img = cv2.stylization(decode_array_to_img, sigma_s = 60, sigma_r = 0.6)
    status, output_image = cv2.imencode('.PNG', converted_water_img)

    return output_image

def inverted_effect(decode_array_to_img):

    inverted_img = cv2.bitwise_not(decode_array_to_img)
    status, output_image = cv2.imencode('.PNG', inverted_img)

    return output_image

def hdr_image(decode_array_to_img):

    hdr_img = cv2.detailEnhance(decode_array_to_img, sigma_s = 12, sigma_r = 0.15)
    status, output_image = cv2.imencode('.PNG', hdr_img)

    return output_image
@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()










