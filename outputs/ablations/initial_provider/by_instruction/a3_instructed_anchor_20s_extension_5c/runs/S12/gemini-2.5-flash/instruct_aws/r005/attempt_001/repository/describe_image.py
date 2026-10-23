from vision_client import VisionClient
from vision_models import ImageRequest, ImageDescriptionResponse, normalize_rekognition_labels
import os

def describe_image(request: ImageRequest) -> ImageDescriptionResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).client
    response = client.detect_labels(
        Image={'Bytes': request.image_bytes},
        MaxLabels=5,
        MinConfidence=80
    )
    labels = normalize_rekognition_labels(response)
    description_parts = [label['name'] for label in labels if label['name']]
    description = ", ".join(description_parts)
    if description:
        description = f"An image containing: {description}."
    else:
        description = "No clear description could be generated for the image."
    return ImageDescriptionResponse(description=description)
