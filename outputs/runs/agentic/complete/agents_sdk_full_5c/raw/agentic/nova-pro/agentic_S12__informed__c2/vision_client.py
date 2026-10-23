import os
from google.cloud import vision

client = vision.ImageAnnotatorClient()

def get_client():
    return client