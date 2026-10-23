import os
from google.cloud import vision_v1p4
from google.cloud.vision_v1p4 import types
from typing import List
from vision_client import get_google_vision_client
from vision_models import ImageInput, LabelResult

def detect_image_labels(image_input: ImageInput) -> List[LabelResult]:
    client = get_google_vision_client()

    if image_input.image_bytes:
        image = types.Image(content=image_input.image_bytes)
    elif image_input.image_url:
        image = types.Image(source=types.ImageSource(image_uri=image_input.image_url))
    else:
        raise ValueError("ImageInput must contain either image_bytes or image_url.")

    features = [types.Feature(type_=types.Feature.Type.LABEL_DETECTION)]
    request = types.AnnotateImageRequest(image=image, features=features)

    response = client.annotate_image(request=request)

    labels = []
    if response.label_annotations:
        for annotation in response.label_annotations:
            labels.append(LabelResult(description=annotation.description, score=annotation.score))
    return labels