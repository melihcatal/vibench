import base64
from vision_client import get_aws_rekognition_client
from vision_models import prepare_image_for_aws, parse_aws_rekognition_labels

def detect_image_labels(image_bytes: bytes):
    client = get_aws_rekognition_client()
    image = prepare_image_for_aws(image_bytes)
    response = client.detect_labels(Image=image, MaxLabels=10, MinConfidence=70)
    return parse_aws_rekognition_labels(response)
