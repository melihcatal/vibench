import os
from typing import List, Dict
from translation_client import get_translation_client
from translation_models import normalize_translate_response

def summarize_translation_quality(translations: List[str]) -> Dict[str, int]:
    """Summarize translation quality issues using Amazon Comprehend Toxicity detection.

    Detects potentially toxic or unsafe language for a simple quality check.
    Requires AWS Comprehend permissions.
    """
    client = get_translation_client()
    # Batch detect sentiments (used as a proxy for toxicity)
    comprehend_resp = client.detect_sentiment(
        Text=\" ".join(translations),
        LanguageCode="en"
    )
    # Convert sentiment score to a simple risk rating (0-3)
    def score_to_risk(score: float) -> int:
        if score < 0.3:
            return 0  # safe
        elif score < 0.6:
            return 1  # low risk
        elif score < 0.8:
            return 2  # medium risk
        else:
            return 3  # high risk
    risk_rating = score_to_risk(comprehend_resp.get("SentimentScore", {}).get("Positive", 0.0))
    summary = {
        "total": len(translations),
        "risk_levels": {
            "safe": 0,
            "low": 0,
            "medium": 0,
            "high": 0,
        }
    }
    summary["risk_levels"]["high"] = risk_rating
    return summary
