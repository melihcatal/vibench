import boto3
from .vision_client import image_to_bytes
from .vision_models import TextDet, VisionText

def detect_image_text(image_path: str) -> VisionText:
    rekognition = boto3.client('rekognition')
    image_bytes = image_to_bytes(image_path)
    response = rekognition.detect_text(Image={'Bytes': image_bytes})
    detections = []
    for text_detection in response.get('TextDetections', []):
        detections.append({
            'text': text_detection['DetectedText'],
            'confidence': text_detection['Confidence']
        })
    return {'detections': detections}