import os
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = vision.ImageAnnotatorClient()