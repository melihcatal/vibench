import os
from typing import Dict, Any
from vision_client import get_vision_client
from vision_models import ImageRequest, SafeSearchDetectionResponse
from google.cloud.vision_v1 import Feature, Image


def score_image_safety(image_request: ImageRequest) -> Dict[str, str]:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision.
    Returns a dictionary of safety ratings (adult, spoof, medical, violence, racy).
    """
    client = get_vision_client()

    image = (
        Image(content=image_request.image_content)
        if image_request.image_content
        else Image(source={"image_uri": image_request.image_uri})
    )

    features = [Feature(type_=Feature.Type.SAFE_SEARCH_DETECTION)]
    response = client.annotate_image({"image": image, "features": features})

    safety_response = SafeSearchDetectionResponse.from_vision_response(response)
    return {
        "adult": safety_response.adult,
        "spoof": safety_response.spoof,
        "medical": safety_response.medical,
        "violence": safety_response.violence,
        "racy": safety_response.racy,
    }
