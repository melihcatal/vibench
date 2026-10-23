import os
from vision_client import VisionClient

def detect_image_labels(image_path):
    client = VisionClient()
    response = client.label_detection(image_path)  # Calls provider's label detection API
    labels = [label.description for label in response]
    return labels