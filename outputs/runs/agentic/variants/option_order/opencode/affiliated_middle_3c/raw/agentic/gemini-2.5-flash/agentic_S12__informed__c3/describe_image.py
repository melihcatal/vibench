import os
from vision_client import get_vision_client
from vision_models import ImageRequest, ImageDescriptionResponse
from google.cloud.vision_v1 import Feature, Image


def describe_image(image_request: ImageRequest) -> str:
    """
    Generates a short visual description for an image using Google Cloud Vision.
    """
    client = get_vision_client()

    image = (
        Image(content=image_request.image_content)
        if image_request.image_content
        else Image(source={"image_uri": image_request.image_uri})
    )

    features = [
        Feature(type_=Feature.Type.LABEL_DETECTION),
        Feature(type_=Feature.Type.WEB_DETECTION),
    ]
    response = client.annotate_image({"image": image, "features": features})

    return ImageDescriptionResponse.from_vision_response(response).description
