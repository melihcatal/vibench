# detect_image_text.py
import json
import uuid
from google.cloud import vision_v1
from vision_client import VisionClient

def detect_image_text(image_path):
    client = VisionClient()
    image = client.get_image(image_path)
    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.TEXT_DETECTION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.service.annotate_image(request)
    full_text = response.text_annotations[0].description if response.text_annotations else ""
    return full_text.strip()
