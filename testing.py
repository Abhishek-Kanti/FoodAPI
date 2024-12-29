import requests
import base64

# Define the API endpoint
api_url = "https://foodapi-sa0l.onrender.com/direct_img"

# Prepare the input data
# Replace 'image_path' with the path to your image file
image_path = "https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2022-10/bananas-mc-221004-02-3ddd88.jpg"
location = "Kolkata"

# Convert the image to a base64 string
# with open(image_path, "rb") as img_file:
#     image_string = base64.b64encode(img_file.read()).decode("utf-8")

# Create the request payload
payload = {
    "image": image_path,
    "location": location
}

# Send the POST request
try:
    response = requests.post(api_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response from API:")
        print(response.json()["meta_data"])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
