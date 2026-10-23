import os
from google.cloud import language_v1
from typing import List, Dict

def check_text_for_safety(text: str) -> Dict[str, str]:
    """
    Checks secret labels and notes for unsafe text using Google Cloud Natural Language API.
    Returns a dictionary indicating safety categories and their scores.
    This example uses sentiment analysis as a proxy for "safety" to demonstrate API usage.
    For actual content moderation, a dedicated moderation API would be used if available.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    try:
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        # A more robust solution would involve content classification/moderation, if available
        # For demonstration, we'll just look at overall sentiment score.
        safety_analysis = {
            "overall_sentiment_score": str(sentiment.score),
            "overall_sentiment_magnitude": str(sentiment.magnitude),
            "safety_flag": "POTENTIALLY_UNSAFE" if sentiment.score < -0.2 or sentiment.magnitude > 1.0 else "SAFE" # Example heuristic
        }
        return safety_analysis
    except Exception as e:
        print(f"Error analyzing text for safety: {e}")
        return {"error": str(e), "safety_flag": "ERROR"}

def check_secret_labels_and_notes(labels: Dict[str, str], notes: str) -> Dict[str, Dict[str, str]]:
    """
    Aggregates safety checks for secret labels and notes.
    """
    results = {}
    for key, value in labels.items():
        results[f"label_{key}"] = check_text_for_safety(value)
    if notes:
        results["notes"] = check_text_for_safety(notes)
    return results
