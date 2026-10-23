from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ImageAnalysisRequest:
    """Standardized request model for image analysis."""
    image_uri: Optional[str] = None
    image_bytes: Optional[bytes] = None
    features: Optional[List[str]] = None  # e.g., ["LABELS", "DESCRIPTION", "TEXT", "SAFETY"]

    def __post_init__(self):
        if not self.image_uri and not self.image_bytes:
            raise ValueError("Either image_uri or image_bytes must be provided.")

@dataclass
class LabelDetectionResult:
    """Result for image label/object detection."""
    labels: List[str]

@dataclass
class ImageDescriptionResult:
    """Result for image visual description."""
    description: Optional[str]
    confidence: Optional[float] = None

@dataclass
class TextDetectionResult:
    """Result for text detection within an image."""
    detected_text: List[str]

@dataclass
class ImageSafetyResult:
    """Result for image content safety scoring."""
    scores: Dict[str, Any]  # e.g., {"violence": 0.9, "adult": 0.1}

@dataclass
class UnifiedImageAnalysisResult:
    """Aggregated results from multiple vision analyses."""
    image_uri: Optional[str] = None
    label_results: Optional[LabelDetectionResult] = None
    description_results: Optional[ImageDescriptionResult] = None
    text_results: Optional[TextDetectionResult] = None
    safety_results: Optional[ImageSafetyResult] = None

if __name__ == '__main__':
    # Example usage of models
    req = ImageAnalysisRequest(image_uri="https://example.com/image.jpg", features=["LABELS"])
    print(f"Request: {req}")

    labels = LabelDetectionResult(labels=["cat", "animal", "pet"])
    print(f"Labels: {labels}")

    description = ImageDescriptionResult(description="A cat sleeping on a couch.", confidence=0.0)
    print(f"Description: {description}")

    agentic_result = UnifiedImageAnalysisResult(
        image_uri="https://example.com/image.jpg",
        label_results=labels,
        description_results=description
    )
    print(f"Unified Result: {agentic_result}")
