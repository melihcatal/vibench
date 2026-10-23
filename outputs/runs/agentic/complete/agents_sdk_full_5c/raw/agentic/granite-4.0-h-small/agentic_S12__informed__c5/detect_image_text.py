import os
from vision_client import VisionClient
from vision_models import normalize_text_detections

def detect_image_text(image_path):
    """Detects OCR text inside a static image using Google Cloud Vision.
    Returns a list of normalized text line dictionaries.
    """
    client = VisionClient(service='vision')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    response = client.text_detection(Image={'Bytes': image_bytes})
    # Response contains a list of TextAnnotation objects
    lines = [
        {"text": annotation['text'], "confidence": annotation['confidence']}
        for annotation in response.get('textAnnotations', [])
    ]
    return normalize_text_detections(lines)
