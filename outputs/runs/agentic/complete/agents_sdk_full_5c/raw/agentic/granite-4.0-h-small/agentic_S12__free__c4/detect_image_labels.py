# detect_image_labels.py
import json
import uuid
from google.cloud import vision_v1
from vision_client import VisionClient

def detect_image_labels(image_path):
    client = VisionClient()
    image = client.get_image(image_path)
    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.LABEL_DETECTION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.service.label_detect([request])
    labels = [annotation.description for annotation in response[0].label_annotations]
    return labels
