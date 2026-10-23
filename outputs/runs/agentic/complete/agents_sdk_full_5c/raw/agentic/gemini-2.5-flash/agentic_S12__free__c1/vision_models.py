from typing import List, Dict, Any

class ImageAnalysisResult:
    """A simple data structure to hold various image analysis results."""
    def __init__(self,
                 image_uri: str,
                 labels: List[str] = None,
                 description: str = None,
                 detected_text: str = None,
                 safety_scores: Dict[str, str] = None):
        self.image_uri = image_uri
        self.labels = labels if labels is not None else []
        self.description = description
        self.detected_text = detected_text
        self.safety_scores = safety_scores if safety_scores is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_uri": self.image_uri,
            "labels": self.labels,
            "description": self.description,
            "detected_text": self.detected_text,
            "safety_scores": self.safety_scores,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return ImageAnalysisResult(
            image_uri=data.get("image_uri"),
            labels=data.get("labels", []),
            description=data.get("description"),
            detected_text=data.get("detected_text"),
            safety_scores=data.get("safety_scores", {}),
        )

if __name__ == '__main__':
    example_result = ImageAnalysisResult(
        image_uri="gs://example-bucket/image.jpg",
        labels=["cat", "animal"],
        description="A fluffy cat sitting on a rug.",
        detected_text="Hello World",
        safety_scores={"adult": "VERY_UNLIKELY", "violence": "UNLIKELY"}
    )
    print("Example ImageAnalysisResult:", example_result.to_dict())

    rehydrated_result = ImageAnalysisResult.from_dict(example_result.to_dict())
    print("Rehydrated Result:", rehydrated_result.to_dict())
