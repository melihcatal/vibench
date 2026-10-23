import boto3
from typing import Dict, Any, List
from vision_client import get_rekognition_client
from vision_models import ImagePayload, ImageDescriptionResponse

def describe_image(payload: ImagePayload, config: Dict[str, Any]) -> ImageDescriptionResponse:
    client = get_rekognition_client(config)
    image_bytes = payload.image_bytes

    # Use detect_labels to get information about the image
    response = client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=int(config.get('max_labels', 10))
    )

    labels = [label['Name'] for label in response.get('Labels', [])]

    description_parts = []
    if labels:
        description_parts.append("An image containing")
        if len(labels) == 1:
            description_parts.append(labels[0])
        else:
            description_parts.append(", ".join(labels[:-1]))
            description_parts.append("and")
            description_parts.append(labels[-1])
    
    if not description_parts:
        description = "An image with no identifiable labels."
    else:
        description = " ".join(description_parts) + "."

    return ImageDescriptionResponse(description=description)
