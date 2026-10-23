import os
from google.cloud import vision_v1
from vision_client import get_vision_client, create_vision_image_object
from vision_models import ImageData, LabelResult

def detect_image_labels(image_data: ImageData) -> list[LabelResult]:
    """
    Detects labels (objects, concepts) in a static image using Google Cloud Vision AI.
    """
    client = get_vision_client()
    image = create_vision_image_object(image_data)

    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.LABEL_DETECTION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append(LabelResult(description=label.description, score=label.score))
    return labels
