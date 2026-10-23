import boto3
from vision_client import load_image_bytes, AWS_REGION
from vision_models import DetectedText

def detect_image_text(image_path: str) -> DetectedText:
    client = boto3.client('rekognition', region_name=AWS_REGION)
    image_bytes = load_image_bytes(image_path)
    response = client.detect_text(Image={'Bytes': image_bytes})
    texts = [detection['DetectedText']['Text'] for detection in response['TextDetections']]
    return DetectedText(texts=texts)