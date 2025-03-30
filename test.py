import requests
import base64

with open("ss.png", "rb") as img_file:
    base64_string = base64.b64encode(img_file.read()).decode("utf-8")

url = "http://127.0.0.1:8000/extract-json"
data = {"image_data": base64_string}

response = requests.post(url, json=data)
print(response.json())