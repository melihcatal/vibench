"""[SAME-SCENARIO] detects text appearing inside an image"""
import boto3
from vision_client import image_to_bytes
from vision_models import TextResponse

def detect_image_text(image_path: str) -> TextResponse:
    # Amazon Rekognition
    rekognition = boto3.client('rekognition')
    content = image_to_bytes(image_path)
    response = rekognition.detect_text(Image={'Bytes': content})
    texts = [detection['DetectedText'] for detection in response['TextDetections']]
    return {'texts': texts}
