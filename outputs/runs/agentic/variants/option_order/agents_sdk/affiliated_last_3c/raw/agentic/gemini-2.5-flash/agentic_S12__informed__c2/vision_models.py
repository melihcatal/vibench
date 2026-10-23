from typing import List, Dict, Any

# This file defines local request, response, and normalization helpers.

class VisionAnalysisRequest:
    """Represents a request for visual analysis."""
    def __init__(self, image_bytes: bytes, image_format: str = "jpeg"):
        self.image_bytes = image_bytes
        self.image_format = image_format

    def to_dict(self):
        return {
            "image_bytes_length": len(self.image_bytes),
            "image_format": self.image_format
        }

class VisionAnalysisResult:
    """Aggregates results from various visual understanding tasks."""
    def __init__(self,
                 labels: List[str] = None,
                 description: str = None,
                 detected_text: List[str] = None,
                 safety_scores: Dict[str, str] = None):
        self.labels = labels if labels is not None else []
        self.description = description if description is not None else ""
        self.detected_text = detected_text if detected_text is not None else []
        self.safety_scores = safety_scores if safety_scores is not None else {}

    def to_dict(self):
        return {
            "labels": self.labels,
            "description": self.description,
            "detected_text": self.detected_text,
            "safety_scores": self.safety_scores
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return VisionAnalysisResult(
            labels=data.get("labels"),
            description=data.get("description"),
            detected_text=data.get("detected_text"),
            safety_scores=data.get("safety_scores")
        )

def normalize_safety_score(score_name: str) -> str:
    """Normalizes Google Cloud Vision Safe Search Likelihood enum names to a simpler string."""
    # Google Cloud Vision uses likelihood enums like UNLIKELY, POSSIBLE, LIKELY, VERY_LIKELY.
    # This is a simple pass-through for now, but could be mapped to LOW, MEDIUM, HIGH, etc.
    return score_name

if __name__ == '__main__':
    # Example usage
    request = VisionAnalysisRequest(image_bytes=b"dummy_image_data", image_format="png")
    print(f"Request dict: {request.to_dict()}")

    result = VisionAnalysisResult(
        labels=["cat", "animal"],
        description="A picture of a cat.",
        detected_text=["MEOW"],
        safety_scores={"adult": "UNLIKELY", "violence": "VERY_UNLIKELY"}
    )
    print(f"Result dict: {result.to_dict()}")

    reconstructed_result = VisionAnalysisResult.from_dict(result.to_dict())
    print(f"Reconstructed result description: {reconstructed_result.description}")
