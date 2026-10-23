import os
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import ImageRequest, LabelDetectionResult, VisionResponse


def detect_image_labels(request: ImageRequest) -> VisionResponse:
    client = get_vision_client()
    image = vision_v1.Image()

    if request.image_content:
        image.content = request.image_content
    elif request.image_uri:
        image.source.image_uri = request.image_uri
    else:
        raise ValueError("Image content or image URI must be provided.")

    response = client.label_detection(image=image)
    labels = [
        LabelDetectionResult(description=label.description, score=label.score)
        for label in response.label_annotations
    ]
    return VisionResponse(labels=labels)
