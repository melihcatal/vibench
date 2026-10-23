import base64
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class StaticImageRequest:
    image_data: Optional[str] = None  # Base64 encoded image data
    image_url: Optional[str] = None   # URL to the image

    def __post_init__(self):
        if not self.image_data and not self.image_url:
            raise ValueError("Either image_data or image_url must be provided.")

@dataclass
class VisualUnderstandingRequest:
    static_image_request: StaticImageRequest
    features: List[str] = field(default_factory=list) # e.g., ["LABELS", "TEXT_DETECTION"]
    model_id: str = "default_vision_model"

@dataclass
class Label:
    description: str
    score: float

@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

@dataclass
class TextAnnotation:
    text: str
    bounding_boxes: List[BoundingBox]

@dataclass
class ImageAnalysisResponse:
    labels: List[Label] = field(default_factory=list)
    text_annotations: List[TextAnnotation] = field(default_factory=list)
    captions: List[str] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

class NormalizationHelper:
    @staticmethod
    def encode_image_to_base64(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    def normalize_response(raw_response: Dict[str, Any]) -> ImageAnalysisResponse:
        labels = []
        if "labelAnnotations" in raw_response:
            for label_data in raw_response["labelAnnotations"]:
                labels.append(Label(description=label_data["description"], score=label_data["score"]))

        text_annotations = []
        if "textAnnotations" in raw_response:
            for text_data in raw_response["textAnnotations"]:
                # Assuming a simplified bounding box for now, actual would be more complex
                text_annotations.append(TextAnnotation(text=text_data["description"], bounding_boxes=[]))
        
        captions = []
        if "fullTextAnnotation" in raw_response:
            captions.append(raw_response["fullTextAnnotation"]["text"])

        return ImageAnalysisResponse(
            labels=labels,
            text_annotations=text_annotations,
            captions=captions,
            raw_response=raw_response
        )
