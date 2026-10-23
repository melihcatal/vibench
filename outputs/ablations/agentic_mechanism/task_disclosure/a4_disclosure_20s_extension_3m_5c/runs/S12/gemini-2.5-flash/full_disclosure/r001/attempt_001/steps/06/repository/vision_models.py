
import base64
from typing import Dict, Any

class ImageRequest:
    def __init__(self, image_data: bytes):
        self.image_data = image_data

    def to_json(self) -> Dict[str, str]:
        return {
            "image_data": base64.b64encode(self.image_data).decode('utf-8')
        }

class ImageResponse:
    def __init__(self, results: Dict[str, Any]):
        self.results = results

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]):
        return cls(results=json_data.get("results", {}))

def normalize_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes the response data from an image analysis service.
    This is a placeholder for actual normalization logic.
    """
    normalized = {
        "status": response_data.get("status", "unknown"),
        "data": response_data.get("data", {})
    }
    return normalized
