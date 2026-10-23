from typing import List, Dict, Any

class ImageAnalysisResult:
    """A simple model to hold aggregated image analysis results."""
    def __init__(self, labels: List[str], description: str, text_content: str, safety_scores: Dict[str, str]):
        self.labels = labels
        self.description = description
        self.text_content = text_content
        self.safety_scores = safety_scores

    def to_dict(self) -> Dict[str, Any]:
        return {
            "labels": self.labels,
            "description": self.description,
            "text_content": self.text_content,
            "safety_scores": self.safety_scores
        }

# No provider-specific imports here, as this is a local helper for models.
# The `ImageAnalysisResult` will be populated by results from provider-specific calls.