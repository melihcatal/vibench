
from typing import List, Dict, Any, Optional

class ImageAnalysisRequest:
    """Represents a request for image analysis."""
    def __init__(self, image_bytes: bytes, image_url: Optional[str] = None):
        self.image_bytes = image_bytes
        self.image_url = image_url

class ImageLabel:
    """Represents a detected label or object in an image."""
    def __init__(self, name: str, confidence: float):
        self.name = name
        self.confidence = confidence

class ImageDescription:
    """Represents a generated visual description for an image."""
    def __init__(self, text: str, confidence: Optional[float] = None):
        self.text = text
        self.confidence = confidence

class DetectedText:
    """Represents text detected within an image."""
    def __init__(self, text: str, bounding_box: Optional[List[float]] = None, confidence: Optional[float] = None):
        self.text = text
        self.bounding_box = bounding_box
        self.confidence = confidence

class ImageSafetyScore:
    """Represents a safety score for an image based on a specific category."""
    def __init__(self, category: str, score: float):
        self.category = category
        self.score = score

class ImageAnalysisResult:
    """Aggregates various image analysis results."""
    def __init__(
        self,
        labels: Optional[List[ImageLabel]] = None,
        description: Optional[ImageDescription] = None,
        detected_text: Optional[List[DetectedText]] = None,
        safety_scores: Optional[List[ImageSafetyScore]] = None,
        raw_response: Optional[Dict[str, Any]] = None
    ):
        self.labels = labels if labels is not None else []
        self.description = description
        self.detected_text = detected_text if detected_text is not None else []
        self.safety_scores = safety_scores if safety_scores is not None else []
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        """Converts the result to a dictionary."""
        return {
            "labels": [label.__dict__ for label in self.labels],
            "description": self.description.__dict__ if self.description else None,
            "detected_text": [text.__dict__ for text in self.detected_text],
            "safety_scores": [score.__dict__ for score in self.safety_scores],
            "raw_response": self.raw_response
        }

if __name__ == '__main__':
    print("This file defines data models for image analysis.")
    # Example usage:
    labels = [ImageLabel(name="cat", confidence=0.95), ImageLabel(name="animal", confidence=0.90)]
    description = ImageDescription(text="A cat sitting on a couch.")
    detected_text = [DetectedText(text="Hello")]
    safety_scores = [ImageSafetyScore(category="gore", score=0.01)]
    
    result = ImageAnalysisResult(
        labels=labels,
        description=description,
        detected_text=detected_text,
        safety_scores=safety_scores
    )
    
    print(result.to_dict())
