
import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class ImageRequest:
    image_bytes: Optional[str] = None
    image_uri: Optional[str] = None

@dataclasses.dataclass
class ImageResponse:
    labels: Optional[List[str]] = None
    text: Optional[str] = None
    safety_scores: Optional[Dict[str, float]] = None
    description: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

class VisionModelNormalizer:
    @staticmethod
    def normalize_labels(response_data: Dict[str, Any]) -> List[str]:
        # Placeholder for actual label normalization logic
        # This would typically parse a provider-specific response structure
        if "responses" in response_data and response_data["responses"]:
            first_response = response_data["responses"][0]
            if "labelAnnotations" in first_response:
                return [label["description"] for label in first_response["labelAnnotations"]]
        return []

    @staticmethod
    def normalize_text(response_data: Dict[str, Any]) -> str:
        # Placeholder for actual text normalization logic
        if "responses" in response_data and response_data["responses"]:
            first_response = response_data["responses"][0]
            if "fullTextAnnotation" in first_response:
                return first_response["fullTextAnnotation"]["text"]
        return ""

    @staticmethod
    def normalize_safety_scores(response_data: Dict[str, Any]) -> Dict[str, float]:
        # Placeholder for actual safety score normalization logic
        if "responses" in response_data and response_data["responses"]:
            first_response = response_data["responses"][0]
            if "safeSearchAnnotation" in first_response:
                return {
                    k: VisionModelNormalizer._convert_likelihood_to_score(v)
                    for k, v in first_response["safeSearchAnnotation"].items()
                }
        return {}
    
    @staticmethod
    def _convert_likelihood_to_score(likelihood: str) -> float:
        # Example conversion for likelihood values (e.g., from Google Cloud Vision API)
        likelihood_map = {
            "UNKNOWN": 0.0,
            "VERY_UNLIKELY": 0.1,
            "UNLIKELY": 0.3,
            "POSSIBLE": 0.5,
            "LIKELY": 0.7,
            "VERY_LIKELY": 0.9,
        }
        return likelihood_map.get(likelihood, 0.0)
