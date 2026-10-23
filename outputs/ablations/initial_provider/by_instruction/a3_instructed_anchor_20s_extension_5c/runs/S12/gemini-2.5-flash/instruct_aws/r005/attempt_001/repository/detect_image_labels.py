from vision_client import VisionClient
from vision_models import ImageLabelRequest, ImageLabelResponse, normalize_rekognition_labels
import os

def detect_image_labels(request: ImageLabelRequest) -> ImageLabelResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).client
    response = client.detect_labels(
        Image={'Bytes': request.image_bytes},
        MaxLabels=10,
        MinConfidence=70
    )
    labels = normalize_rekognition_labels(response)
    return ImageLabelResponse(labels=labels)
