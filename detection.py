import requests

backend_url = 'https://det-backendv2-497430069448.us-central1.run.app/predict/'


with open('test_image.jpg', "rb") as img:
    files = {"file": img}
    response = requests.post(backend_url, files=files)

response.json()