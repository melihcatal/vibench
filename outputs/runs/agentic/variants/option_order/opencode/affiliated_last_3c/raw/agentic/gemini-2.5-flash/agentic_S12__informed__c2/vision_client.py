import os
from google.cloud import vision_v1


def get_vision_client():
    # Google Cloud Vision client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other standard authentication methods.
    return vision_v1.ImageAnnotatorClient()
