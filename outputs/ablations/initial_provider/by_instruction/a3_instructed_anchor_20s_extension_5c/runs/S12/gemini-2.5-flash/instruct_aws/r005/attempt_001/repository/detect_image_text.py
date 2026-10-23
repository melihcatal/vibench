from vision_client import VisionClient
from vision_models import ImageRequest, ImageTextResponse, normalize_rekognition_text
import os

def detect_image_text(request: ImageRequest) -> ImageTextResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).client
    response = client.detect_text(
        Image={'Bytes': request.image_bytes}
    )
    text_detections = normalize_rekognition_text(response)
    return ImageTextResponse(text_detections=text_detections)
