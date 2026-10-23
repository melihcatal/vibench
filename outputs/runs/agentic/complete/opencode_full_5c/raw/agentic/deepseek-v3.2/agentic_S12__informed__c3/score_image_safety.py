import os
from typing import Dict, Any
from vision_client import VisionClient
from vision_models import SafetyScoreResult
from google.cloud import vision


def score_image_safety(image_path: str, credentials_path: str = None) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_path(image_path)

    features = [vision.Feature(type_=vision.Feature.Type.SAFE_SEARCH_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = SafetyScoreResult.from_google_vision(response)
    return {
        "safe_search_annotation": result.safe_search_annotation,
        "is_safe": result.is_safe,
    }


def score_image_safety_from_bytes(
    image_bytes: bytes, credentials_path: str = None
) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_bytes(image_bytes)

    features = [vision.Feature(type_=vision.Feature.Type.SAFE_SEARCH_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = SafetyScoreResult.from_google_vision(response)
    return {
        "safe_search_annotation": result.safe_search_annotation,
        "is_safe": result.is_safe,
    }


def score_image_safety_from_uri(
    image_uri: str, credentials_path: str = None
) -> Dict[str, Any]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_uri(image_uri)

    features = [vision.Feature(type_=vision.Feature.Type.SAFE_SEARCH_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = SafetyScoreResult.from_google_vision(response)
    return {
        "safe_search_annotation": result.safe_search_annotation,
        "is_safe": result.is_safe,
    }
