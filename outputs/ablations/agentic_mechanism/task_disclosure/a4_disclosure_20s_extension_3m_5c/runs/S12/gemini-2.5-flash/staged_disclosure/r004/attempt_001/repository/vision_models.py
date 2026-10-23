
import base64
from typing import Dict, Any

class StaticImageRequest:
    """
    Represents a local request for static image analysis.
    Assumes image content is base64 encoded for simplicity.
    """
    def __init__(self) -> None:
        self.image_data: str = "" # Base64 encoded image string
        self.features: Dict[str, Any] = {} # e.g., {"LABEL_DETECTION": {}, "OBJECT_LOCALIZATION": {}}

    def from_file(self, image_path: str) -> None:
        with open(image_path, "rb") as image_file:
            self.image_data = base64.b64encode(image_file.read()).decode("utf-8")

    def to_json(self) -> Dict[str, Any]:
        return {
            "image": {"content": self.image_data},
            "features": [{"type": k, **v} for k, v in self.features.items()]
        }

class VisualUnderstandingResponse:
    """
    Represents a local response from a visual understanding model.
    """
    def __init__(self, raw_response: Dict[str, Any]) -> None:
        self.raw_response = raw_response
        self.labels: list[str] = []
        self.objects: list[Dict[str, Any]] = []
        self._parse_response()

    def _parse_response(self) -> None:
        if "labelAnnotations" in self.raw_response:
            self.labels = [label["description"] for label in self.raw_response["labelAnnotations"]]
        if "localizedObjectAnnotations" in self.raw_response:
            self.objects = self.raw_response["localizedObjectAnnotations"]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "labels": self.labels,
            "objects": self.objects,
            "full_response": self.raw_response
        }

def normalize_image_data(image_bytes: bytes) -> bytes:
    """
    Placeholder for image data normalization.
    In a real scenario, this might involve resizing,
    color correction, or format conversion.
    For this local helper, it simply returns the bytes as is.
    """
    # Example: could use PIL/Pillow for actual image processing
    # from PIL import Image
    # import io
    # image = Image.open(io.BytesIO(image_bytes))
    # # Perform operations like resize, convert to RGB, etc.
    # # image = image.resize((224, 224))
    # output_buffer = io.BytesIO()
    # image.save(output_buffer, format="JPEG")
    # return output_buffer.getvalue()
    return image_bytes

