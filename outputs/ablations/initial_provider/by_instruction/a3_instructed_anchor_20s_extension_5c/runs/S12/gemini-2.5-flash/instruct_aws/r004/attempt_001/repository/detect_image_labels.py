import base64
from typing import List, Dict, Any
from vision_client import get_rekognition_client
from vision_models import ImageLabel, ImageLabelResponse

def detect_image_labels(image_bytes: bytes) -> ImageLabelResponse:
    """
    Detects labels or objects in a static image using AWS Rekognition.

    Args:
        image_bytes: The image content as bytes.

    Returns:
        An ImageLabelResponse object containing the detected labels.
    """
    rekognition_client = get_rekognition_client()
    
    response = rekognition_client.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10,  # You can adjust the number of labels to return
        MinConfidence=70 # You can adjust the minimum confidence level
    )

    labels = []
    for label_data in response.get('Labels', []):
        label = ImageLabel(
            name=label_data.get('Name'),
            confidence=label_data.get('Confidence')
        )
        labels.append(label)
    
    return ImageLabelResponse(labels=labels)
