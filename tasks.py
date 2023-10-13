from celery import Celery
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Use the URL of your Redis server
    backend="redis://localhost:6379/0",
)

# Cloudinary configuration
import cloudinary

cloudinary.config(
    cloud_name="YOUR_CLOUD_NAME", api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET"
)


# Define a function to upload the image to Cloudinary
def upload_to_cloudinary(image):
    result = upload(image, folder="products")  # Specify the "products" folder
    return cloudinary_url(result["public_id"], format=result["format"])[0]


@app.task
def process_image_and_store_data(data, image):
    print(data)
    print(image)
    # name = data['name']
    # price = data['price']
    # discounted_price = data['discounted_price']

    # # Upload the image to Cloudinary
    # image_url = upload_to_cloudinary(image)

    # Your logic to process the data, e.g., saving to a CSV file
    # Replace this with your actual data processing and CSV writing logic

    # For demonstration, we print the data and image URL
    # print("Name:", name)
    # print("Price:", price)
    # print("Discounted Price:", discounted_price)
    # print("Image URL:", image_url)
