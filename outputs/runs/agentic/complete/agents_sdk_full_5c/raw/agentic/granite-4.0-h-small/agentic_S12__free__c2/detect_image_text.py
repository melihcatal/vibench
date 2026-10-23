import os
from vision_client import VisionClient

def detect_image_text(image_path):
    client = VisionClient()
    response = client.text_extraction(image_path)  # Calls provider's OCR/Text detection API
    # Assume response is a list of text blocks with .text field
    texts = [block.text for block in response]
    return texts
