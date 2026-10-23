import dataclasses
from typing import List, Dict, Any

# Provider: Google Cloud Vertex AI (generativeai.harm_text)
# This file provides local helpers for Text Content Safety,
# conceptually based on Google Cloud's content moderation services.

@dataclasses.dataclass
class TextSafetyRequest:
    """Represents a request for text content safety analysis."""
    text_content: str
    client_id: str = "default_client"

@dataclasses.dataclass
class SafetyRating:
    """Represents a safety rating for a specific category."""
    category: str  # e.g., "HARM_CATEGORY_TOXICITY"
    probability: str  # e.g., "NEGLIGIBLE", "LOW", "MEDIUM", "HIGH"
    score: float # a numerical score, typically between 0.0 and 1.0

@dataclasses.dataclass
class TextSafetyResponse:
    """Represents a response from a text content safety service."""
    safety_ratings: List[SafetyRating]
    processed_text: str = "" # Potentially processed or redacted text

def normalize_safety_response(response_data: Dict[str, Any]) -> TextSafetyResponse:
    """
    Normalizes a raw API response dictionary into a TextSafetyResponse object.
    This is a simplified example, real-world normalization might be more complex.
    """
    safety_ratings = []
    for rating_data in response_data.get("safety_ratings", []):
        safety_ratings.append(
            SafetyRating(
                category=rating_data.get("category", "UNKNOWN"),
                probability=rating_data.get("probability", "UNKNOWN"),
                score=rating_data.get("score", 0.0)
            )
        )
    processed_text = response_data.get("processed_text", "")
    return TextSafetyResponse(safety_ratings=safety_ratings, processed_text=processed_text)
