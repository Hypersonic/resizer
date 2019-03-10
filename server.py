from flask import Flask, render_template, send_file, request, flash, redirect, url_for
from os import environ
from PIL import Image
import os.path
import random
import warnings
from io import BytesIO


def secret_key():
    if not os.path.exists(".secret_key"):
        with open(".secret_key", "wb") as f:
            f.write(bytes([random.randint(0, 255) for _ in range(1024)]))
    with open(".secret_key", "rb") as f:
        return f.read()


app = Flask(__name__)
app.secret_key = secret_key()
warnings.simplefilter("error", Image.DecompressionBombWarning)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resize", methods=["POST"])
def resize():
    image_file = request.files.get("image")
    size_px = request.form.get("size_px")

    def is_int(value):
        try:
            int(value)
            return True
        except:
            return False

    constraints = (
        ((lambda image, _: image is not None), "You must upload an image!"),
        ((lambda _, size: size is not None), "You must specify a size!"),
        ((lambda _, size: is_int(size)), "Size must be an integer!"),
        ((lambda _, size: int(size) > 0), "Size must be positive!"),
    )

    for predicate, error in constraints:
        if not predicate(image_file, size_px):
            flash("Error: {}".format(error))
            return redirect(url_for("index"))

    size = int(size_px)
    image = Image.open(image_file)
    resized = image.resize((size, size))
    png = BytesIO()
    resized.save(png, format="png")
    png.seek(0)
    return send_file(png, mimetype="image/png")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug="DEBUG" in environ)
