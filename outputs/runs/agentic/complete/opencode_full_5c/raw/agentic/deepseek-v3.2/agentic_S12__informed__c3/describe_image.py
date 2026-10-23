import os
from typing import Dict, Any
from vision_client import VisionClient
from vision_models import ImageDescriptionResult
from google.cloud import vision


def describe_image(image_path: str, credentials_path: str = None) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_path(image_path)

    features = [
        vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
        vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION),
    ]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = ImageDescriptionResult.from_google_vision(response)
    return {"description": result.description, "captions": result.captions}


def describe_image_from_bytes(
    image_bytes: bytes, credentials_path: str = None
) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_bytes(image_bytes)

    features = [
        vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
        vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION),
    ]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = ImageDescriptionResult.from_google_vision(response)
    return {"description": result.description, "captions": result.captions}


def describe_image_from_uri(
    image_uri: str, credentials_path: str = None
) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_uri(image_uri)

    features = [
        vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
        vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION),
    ]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = ImageDescriptionResult.from_google_vision(response)
    return {"description": result.description, "captions": result.captions}
