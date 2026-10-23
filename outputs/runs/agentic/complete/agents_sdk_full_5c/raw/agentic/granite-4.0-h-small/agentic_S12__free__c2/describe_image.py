import os
from vision_client import VisionClient

def describe_image(image_path):
    client = VisionClient()
    response = client.annotate_image(image_path)  # Calls provider's image description endpoint
    # Assume response has a .description field with short caption
    return response.description
