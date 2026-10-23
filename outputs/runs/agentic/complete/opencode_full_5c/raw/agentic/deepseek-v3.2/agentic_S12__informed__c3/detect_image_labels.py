import os
from typing import List, Dict, Any
from vision_client import VisionClient
from vision_models import LabelDetectionResult
from google.cloud import vision


def detect_image_labels(
    image_path: str, credentials_path: str = None
) -> List[Dict[str, Any]]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_path(image_path)

    features = [vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = LabelDetectionResult.from_google_vision(response)
    return result.labels


def detect_image_labels_from_bytes(
    image_bytes: bytes, credentials_path: str = None
) -> List[Dict[str, Any]]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_bytes(image_bytes)

    features = [vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = LabelDetectionResult.from_google_vision(response)
    return result.labels


def detect_image_labels_from_uri(
    image_uri: str, credentials_path: str = None
) -> List[Dict[str, Any]]:
    client = VisionClient(credentials_path)
    image = client.load_image_from_uri(image_uri)

    features = [vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION)]
    request = vision.AnnotateImageRequest(image=image, features=features)

    response = client.client.annotate_image(request=request)

    result = LabelDetectionResult.from_google_vision(response)
    return result.labels
