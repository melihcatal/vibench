from vision_client import VisionClient
from vision_models import ImageRequest, ImageSafetyResponse, normalize_rekognition_moderation_labels
import os

def score_image_safety(request: ImageRequest) -> ImageSafetyResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).client
    response = client.detect_moderation_labels(
        Image={'Bytes': request.image_bytes}
    )
    moderation_labels = normalize_rekognition_moderation_labels(response)
    return ImageSafetyResponse(moderation_labels=moderation_labels)
