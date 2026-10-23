
from typing import Dict, Any, List, Union

class StaticImageRequest:
    def __init__(self, image_data: str, features: List[str]):
        self.image_data = image_data  # Base64 encoded image
        self.features = features      # e.g., ["LABELS", "SAFE_SEARCH"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_data": self.image_data,
            "features": self.features
        }

class StaticImageResponse:
    def __init__(self, raw_response: Dict[str, Any]):
        self.raw_response = raw_response
        self.labels = raw_response.get("labelAnnotations", [])
        self.safe_search = raw_response.get("safeSearchAnnotation", {})

    def to_dict(self) -> Dict[str, Any]:
        return self.raw_response

class VisualUnderstandingRequest:
    def __init__(self, image_data: str, prompt: str):
        self.image_data = image_data  # Base64 encoded image
        self.prompt = prompt          # Text prompt for understanding

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_data": self.image_data,
            "prompt": self.prompt
        }

class VisualUnderstandingResponse:
    def __init__(self, raw_response: Dict[str, Any]):
        self.raw_response = raw_response
        self.text_annotations = raw_response.get("textAnnotations", [])

    def to_dict(self) -> Dict[str, Any]:
        return self.raw_response

def normalize_static_image_request(request: StaticImageRequest) -> Dict[str, Any]:
    """
    Normalizes a StaticImageRequest object into a dictionary suitable for API consumption.
    """
    return request.to_dict()

def normalize_static_image_response(response_dict: Dict[str, Any]) -> StaticImageResponse:
    """
    Normalizes a raw API response dictionary into a StaticImageResponse object.
    """
    return StaticImageResponse(response_dict)

def normalize_visual_understanding_request(request: VisualUnderstandingRequest) -> Dict[str, Any]:
    """
    Normalizes a VisualUnderstandingRequest object into a dictionary suitable for API consumption.
    """
    return request.to_dict()

def normalize_visual_understanding_response(response_dict: Dict[str, Any]) -> VisualUnderstandingResponse:
    """
    Normalizes a raw API response dictionary into a VisualUnderstandingResponse object.
    """
    return VisualUnderstandingResponse(response_dict)
