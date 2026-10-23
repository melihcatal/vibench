
import base64
from typing import Dict, Any, List, Optional

class StaticImageRequest:
    def __init__(self, image_data_base64: str, features: Optional[List[str]] = None):
        self.image_data_base64 = image_data_base64
        self.features = features if features is not None else []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_data_base64": self.image_data_base64,
            "features": self.features
        }

    @staticmethod
    def from_file(image_path: str, features: Optional[List[str]] = None) -> 'StaticImageRequest':
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return StaticImageRequest(image_data_base64=encoded_string, features=features)

class StaticImageResponse:
    def __init__(self, response_data: Dict[str, Any]):
        self.response_data = response_data

    def get_labels(self) -> List[str]:
        # Placeholder for extracting labels from a hypothetical API response
        return self.response_data.get("labels", [])

    def get_objects(self) -> List[Dict[str, Any]]:
        # Placeholder for extracting objects from a hypothetical API response
        return self.response_data.get("objects", [])

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StaticImageResponse':
        return StaticImageResponse(response_data=data)

class VisualUnderstandingRequest:
    def __init__(self, image_data_base64: str, context: Optional[str] = None, question: Optional[str] = None):
        self.image_data_base64 = image_data_base64
        self.context = context
        self.question = question

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_data_base64": self.image_data_base64,
            "context": self.context,
            "question": self.question
        }

    @staticmethod
    def from_file(image_path: str, context: Optional[str] = None, question: Optional[str] = None) -> 'VisualUnderstandingRequest':
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return VisualUnderstandingRequest(image_data_base64=encoded_string, context=context, question=question)


class VisualUnderstandingResponse:
    def __init__(self, response_data: Dict[str, Any]):
        self.response_data = response_data

    def get_answer(self) -> Optional[str]:
        # Placeholder for extracting an answer from a hypothetical API response
        return self.response_data.get("answer")

    def get_confidence(self) -> Optional[float]:
        # Placeholder for extracting confidence from a hypothetical API response
        return self.response_data.get("confidence")

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'VisualUnderstandingResponse':
        return VisualUnderstandingResponse(response_data=data)

# Normalization helpers (can be standalone functions or methods within classes)
def normalize_static_image_response(raw_response: Dict[str, Any]) -> StaticImageResponse:
    # This function would take a raw API response and normalize it into StaticImageResponse
    # For now, it simply uses the from_dict constructor.
    return StaticImageResponse.from_dict(raw_response)

def normalize_visual_understanding_response(raw_response: Dict[str, Any]) -> VisualUnderstandingResponse:
    # This function would take a raw API response and normalize it into VisualUnderstandingResponse
    # For now, it simply uses the from_dict constructor.
    return VisualUnderstandingResponse.from_dict(raw_response)
