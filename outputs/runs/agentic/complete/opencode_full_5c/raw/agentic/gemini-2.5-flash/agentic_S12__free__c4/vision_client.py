from google.cloud import vision
import os


def get_vision_client():
    return vision.ImageAnnotatorClient()


def get_image_from_uri(image_uri):
    return vision.Image(source=vision.ImageSource(image_uri=image_uri))


def get_image_from_content(image_content):
    return vision.Image(content=image_content)
