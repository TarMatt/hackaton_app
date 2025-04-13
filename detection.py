import requests
import argparse

backend_url = 'https://det-backendv2-497430069448.us-central1.run.app/predict/'

parser = argparse.ArgumentParser(description="Pass the image file path")
parser.add_argument('file_path', type=str, help="The file path to the image")

args = parser.parse_args()
path = args.file_path

with open(path, "rb") as img:
    files = {"file": img}
    response = requests.post(backend_url, files=files)

print(response.json())