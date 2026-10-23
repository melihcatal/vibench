import os
from typing import List
from vision_client import get_vision_client
from vision_models import ImageRequest, LabelDetectionResponse
from google.cloud.vision_v1 import Feature, Image


def detect_image_labels(image_request: ImageRequest) -> List[str]:
    """
    Detects labels or objects in a static image using Google Cloud Vision.
    """
    client = get_vision_client()

    image = (
        Image(content=image_request.image_content)
        if image_request.image_content
        else Image(source={"image_uri": image_request.image_uri})
    )

    features = [Feature(type_=Feature.Type.LABEL_DETECTION)]
    response = client.annotate_image({"image": image, "features": features})

    return LabelDetectionResponse.from_vision_response(response).labels
