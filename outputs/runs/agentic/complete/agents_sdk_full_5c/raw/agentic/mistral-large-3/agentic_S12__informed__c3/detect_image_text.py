import boto3
from vision_client import get_image_bytes
from vision_models import TextDetectionResponse

def detect_text(image_path: str) -> TextDetectionResponse:
    client = boto3.client('rekognition')
    image_bytes = get_image_bytes(image_path)
    response = client.detect_text(Image={'Bytes': image_bytes})
    
    texts = [text['DetectedText'] for text in response['TextDetections'] if text['Type'] == 'LINE']
    return TextDetectionResponse(
        provider="amazon_rekognition",
        texts=texts,
        raw_response=response
    )