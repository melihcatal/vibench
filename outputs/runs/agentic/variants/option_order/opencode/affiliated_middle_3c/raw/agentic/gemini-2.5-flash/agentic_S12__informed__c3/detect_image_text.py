import os
from vision_client import get_vision_client
from vision_models import ImageRequest, TextDetectionResponse
from google.cloud.vision_v1 import Feature, Image


def detect_image_text(image_request: ImageRequest) -> str:
    """
    Detects text appearing inside an image using Google Cloud Vision.
    """
    client = get_vision_client()

    image = (
        Image(content=image_request.image_content)
        if image_request.image_content
        else Image(source={"image_uri": image_request.image_uri})
    )

    features = [Feature(type_=Feature.Type.TEXT_DETECTION)]
    response = client.annotate_image({"image": image, "features": features})

    return TextDetectionResponse.from_vision_response(response).text
