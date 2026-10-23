from typing import List, Dict, Any

class ImageAnalysisRequest:
    """
    A simple model for encapsulating an image analysis request.
    Could be extended with image URLs, GCS URIs, etc.
    """
    def __init__(self, image_content: bytes):
        self.image_content = image_content

class ImageAnalysisResponse:
    """
    A normalized response model for various image analysis results.
    """
    def __init__(self,
                 labels: List[str] = None,
                 description: str = None,
                 detected_text: str = None,
                 safety_scores: Dict[str, Any] = None):
        self.labels = labels if labels is not None else []
        self.description = description if description is not None else ""
        self.detected_text = detected_text if detected_text is not None else ""
        self.safety_scores = safety_scores if safety_scores is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "labels": self.labels,
            "description": self.description,
            "detected_text": self.detected_text,
            "safety_scores": self.safety_scores
        }
