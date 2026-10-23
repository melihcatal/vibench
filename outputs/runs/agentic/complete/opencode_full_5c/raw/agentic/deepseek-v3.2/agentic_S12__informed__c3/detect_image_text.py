import os
from typing import List, Dict, Any, Optional
from vision_client import VisionClient
from vision_models import TextDetectionResult
from google.cloud import vision


def detect_image_text(image_path: str, credentials_path: str = None) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_path(image_path)

    features = [vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = TextDetectionResult.from_google_vision(response)
    return {"texts": result.texts, "full_text": result.full_text}


def detect_image_text_from_bytes(
    image_bytes: bytes, credentials_path: str = None
) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_bytes(image_bytes)

    features = [vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = TextDetectionResult.from_google_vision(response)
    return {"texts": result.texts, "full_text": result.full_text}


def detect_image_text_from_uri(
    image_uri: str, credentials_path: str = None
) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_uri(image_uri)

    features = [vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = TextDetectionResult.from_google_vision(response)
    return {"texts": result.texts, "full_text": result.full_text}
