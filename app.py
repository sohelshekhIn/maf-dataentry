import cloudinary
from flask import Flask, render_template, request, redirect, url_for, jsonify
from cloudinary.uploader import upload
from os import getenv
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = getenv("SUPABASE_URL")
key: str = getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

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


@app.route("/products")
def products():
    response = supabase.table("products").select("*").execute()
    return render_template("products.html", response=response)


@app.route("/upload", methods=["POST"])
def upload_image():
    # Get the uploaded image and other data
    image = request.files["image"]
    name = request.form["name"]
    price = request.form["price"]
    discounted_price = request.form["discounted_price"]

    # Upload the image to Cloudinary
    result = upload(image, folder="products")
    image_url = result["secure_url"]

    data, count = (
        supabase.table("products")
        .insert(
            {
                "name": name.title(),
                "price": price,
                "disc_price": discounted_price,
                "photo_url": image_url,
            }
        )
        .execute()
    )
    return redirect(url_for("index"))


@app.route("/wa-upload", methods=["POST"])
def automateUpload():
    # get data from request
    data = request.get_json()
    # Get the uploaded image and other data
    image = data["image"]
    name = data["name"]
    price = data["price"]
    discounted_price = data["discounted_price"]
    # Upload the image to Cloudinary
    result = upload(image, folder="products")
    image_url = result["secure_url"]

    data, count = (
        supabase.table("products")
        .insert(
            {
                "name": name.title(),
                "price": price,
                "disc_price": discounted_price,
                "photo_url": image_url,
            }
        )
        .execute()
    )
    return "Done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
