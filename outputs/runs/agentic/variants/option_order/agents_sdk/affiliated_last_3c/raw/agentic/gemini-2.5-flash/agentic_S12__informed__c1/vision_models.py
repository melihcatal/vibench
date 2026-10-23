from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ImageAnalysisResult:
    """A dataclass to hold normalized results from various image analysis tasks."""
    image_uri: str
    labels: List[str] = field(default_factory=list)
    description: Optional[str] = None
    detected_text: Optional[str] = None
    safety_scores: Dict[str, str] = field(default_factory=dict)
    raw_response: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the ImageAnalysisResult object to a dictionary."""
        return {
            "image_uri": self.image_uri,
            "labels": self.labels,
            "description": self.description,
            "detected_text": self.detected_text,
            "safety_scores": self.safety_scores,
            "raw_response": self.raw_response,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Creates an ImageAnalysisResult object from a dictionary."""
        return cls(
            image_uri=data.get("image_uri", ""),
            labels=data.get("labels", []),
            description=data.get("description"),
            detected_text=data.get("detected_text"),
            safety_scores=data.get("safety_scores", {}),
            raw_response=data.get("raw_response", {}),
        )

if __name__ == '__main__':
    # Example usage
    result = ImageAnalysisResult(
        image_uri="gs://my-bucket/image.jpg",
        labels=["cat", "animal"],
        description="An image of a cat.",
        safety_scores={'adult': 'VERY_UNLIKELY'},
    )
    print(result)
    print(result.to_dict())
    
    reconstructed_result = ImageAnalysisResult.from_dict(result.to_dict())
    print(reconstructed_result)
