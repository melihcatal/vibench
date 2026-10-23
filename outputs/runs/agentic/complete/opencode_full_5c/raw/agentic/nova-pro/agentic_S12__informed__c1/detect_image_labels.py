import os
from dashscope import Vision


def detect_image_labels(image_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = Vision(api_key=api_key)
    response = client.detect_labels(image_path)
    return response.labels
