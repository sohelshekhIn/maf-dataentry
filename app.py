import cloudinary
from flask import Flask, render_template, request, redirect, url_for, jsonify
from cloudinary.uploader import upload
import csv
from os import getenv
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

cloudinary.config(
    cloud_name=getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=getenv("CLOUDINARY_API_KEY"),
    api_secret=getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/camera")
def camera():
    return render_template("camera.html")


@app.route("/upload", methods=["POST"])
def upload_image():
    print(request.form)
    # Get the uploaded image and other data
    image = request.files["image"]
    name = request.form["name"]
    price = request.form["price"]
    discounted_price = request.form["discounted_price"]

    # Upload the image to Cloudinary
    result = upload(image, folder="products")
    image_url = result["secure_url"]

    # Create a new CSV entry
    with open("products.csv", mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([name, price, discounted_price, image_url])

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
