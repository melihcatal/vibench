import os
import dashscope


def configure_vision_client():
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


def create_vision_request(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    return image_data
