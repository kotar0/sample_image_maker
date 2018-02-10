import os
from io import BytesIO
from flask import Flask, jsonify, helpers
from PIL import Image, ImageDraw, ImageFont
import random

app = Flask(__name__)


@app.route("/images/<string:category>/<string:width_height>", methods=['GET'])
def maker(category, width_height):
    """
    Make Sample Image
    :param category:
    :param width_height:
    :return: Content-type=Image
    """
    (width, height) = width_height.split("x")
    buf = make_image(category, width, height)
    response = helpers.make_response(buf.getvalue())
    response.headers["Content-type"] = "Image"
    return response


@app.route("/images/categories", methods=['GET'])
def category():
    """
    Get Image Categories
    :return: categories list
    """
    result = os.listdir("static")
    return jsonify(categories=result)


def make_image(category, width, height):
    """
    Make Sample Image(byte)
    :param category:
    :param width:
    :param height:
    :return: Image(byte)
    """
    width = int(width)
    height = int(height)

    original_image_files = os.listdir(os.path.join("static", category))
    count_original_image_files = len(original_image_files)
    random_numbar_for_pick_file = random.randint(0, count_original_image_files)

    original_image_file_name = original_image_files[random_numbar_for_pick_file]
    original_image_file_path = os.path.join("static", category, original_image_file_name)
    if not os.path.isfile(original_image_file_path):
        return None

    img = Image.open(original_image_file_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font/Lovelo Black.otf", int(width/10 + height/10))
    draw.text((width/10, height/10), "SAMPLE", font=font, fill=(255, 255, 255, 100))
    #img.thumbnail((int(width), int(height)))
    img = img.resize((width, height))
    buf = BytesIO()
    img.save(buf, 'png')
    img.close()

    return buf


if __name__ == "__main__":
    app.run(debug=True)