import os
from dashscope import Vision


def describe_image(image_path):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    client = Vision(api_key=api_key)
    response = client.describe_image(image_path)
    return response.description
