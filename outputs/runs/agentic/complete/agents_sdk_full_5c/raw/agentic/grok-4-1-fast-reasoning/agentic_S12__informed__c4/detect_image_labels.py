import argparse
import json
import os
from google.cloud import vision_v1
from typing import List
from vision_client import image_to_bytes
from vision_models import ImageLabels

def detect_image_labels(image_path: str) -> ImageLabels:
    client = vision_v1.ImageAnnotatorClient()
    image = vision_v1.Image(content=image_to_bytes(image_path))
    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    scores = [label.score for label in response.label_annotations]
    return {'labels': labels, 'confidence_scores': scores}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect labels in image using Google Cloud Vision')
    parser.add_argument('image_path', help='Path to input image')
    args = parser.parse_args()
    result = detect_image_labels(args.image_path)
    print(json.dumps(result, indent=2))