
import base64
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class StaticImageRequest:
    image_bytes: bytes
    features: Dict[str, Any]

@dataclass
class VisualUnderstandingRequest:
    image_uri: str
    features: Dict[str, Any]

@dataclass
class VisionResponse:
    raw_response: Dict[str, Any]

def normalize_static_image_request(image_data: bytes, detection_features: list[str]) -> StaticImageRequest:
    """
    Normalizes static image data into a StaticImageRequest object.
    In a real scenario, this would format the request for a specific vision API,
    e.g., Google Cloud Vision API.
    """
    features = {feature: {} for feature in detection_features}
    return StaticImageRequest(image_bytes=image_data, features=features)

def normalize_visual_understanding_request(image_uri: str, understanding_features: list[str]) -> VisualUnderstandingRequest:
    """
    Normalizes image URI and features into a VisualUnderstandingRequest object.
    Similar to static image, this would format for a specific vision API.
    """
    features = {feature: {} for feature in understanding_features}
    return VisualUnderstandingRequest(image_uri=image_uri, features=features)

def parse_vision_response(response_json: Dict[str, Any]) -> VisionResponse:
    """
    Parses a raw JSON response from a vision API into a VisionResponse object.
    """
    return VisionResponse(raw_response=response_json)

def encode_image_to_base64(image_path: str) -> str:
    """
    Encodes an image file to a base64 string.
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string
