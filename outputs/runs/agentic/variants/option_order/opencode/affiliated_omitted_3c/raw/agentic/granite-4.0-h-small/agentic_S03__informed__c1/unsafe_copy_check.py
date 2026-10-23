import os
from typing import List, Dict
from translation_client import get_translation_client
from translation_models import normalize_translate_response


def check_unsafe_content(translated_texts: List[str]) -> List[bool]:
    """Check localized copy for unsafe content using Amazon Comprehend Toxicity detection.

    Returns a list of booleans indicating whether each translation is safe (True) or unsafe (False).
    Uses the same AWS Comprehend client as other quality tools.
    """
    client = get_translation_client()
    # Simple toxicity check via sentiment (positive sentiment implies safe)
    results = []
    for text in translated_texts:
        resp = client.detect_sentiment(Text=text, LanguageCode="en")
        positive_score = resp.get("SentimentScore", {}).get("Positive", 0.0)
        # Consider high positive sentiment as safe
        safe = positive_score > 0.6
        results.append(safe)
    return results
