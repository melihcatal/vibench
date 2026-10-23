from typing import List, Dict, Any

# Request model – normalize incoming text into provider payload
Response = Dict[str, Any]

Request = Dict[str, Any]


def build_request(text: str) -> Request:
    """Create a provider‑specific request payload from raw text.

    Adjust the structure to match the target service (e.g., Amazon Comprehend,
    Alibaba Content Moderation, Perspective API, etc.).
    """
    # Example: Amazon Comprehend / Bedrock Guardrails payload
    return {
        "Text": text,
        "LanguageCode": "en",
    }


def normalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert generic provider response into a unified format used by higher‑level modules.

    Unified format (example):
    {
        'toxicity': 0.73,
        'harassment': 0.12,
        # ... other categories
    }
    """
    # Placeholder – map only the fields that exist in the raw response
    return {
        "toxicity": raw.get("SentimentScore", {}).get("Positive", 0.0),
        "harassment": raw.get("Violations", {}).get("Harassment", 0.0),
        # add other normalization as needed
    }
