import os
from google.cloud import language_v1


def check_content_safety(text):
    """Check narration scripts for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text,
        type_=language_v1.Document.Type.PLAIN_TEXT,
    )

    response = client.analyze_sentiment(request={"document": document})

    safety_analysis = {
        "text": text,
        "sentiment_score": response.document_sentiment.score,
        "sentiment_magnitude": response.document_sentiment.magnitude,
        "is_negative": response.document_sentiment.score < -0.5,
        "is_high_magnitude": response.document_sentiment.magnitude > 2.0,
    }

    try:
        classify_response = client.classify_text(request={"document": document})
        categories = []
        for category in classify_response.categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )
        safety_analysis["categories"] = categories
    except Exception:
        safety_analysis["categories"] = []

    return safety_analysis


def check_toxicity(text):
    """Check for toxic content using Perspective API (Google's toxicity detection)."""
    import requests
    import json

    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=data)
    result = response.json()

    if "attributeScores" in result:
        scores = {}
        for attr, score_data in result["attributeScores"].items():
            scores[attr] = score_data["summaryScore"]["value"]

        return {
            "text": text,
            "toxicity_scores": scores,
            "is_toxic": scores.get("TOXICITY", 0) > 0.7,
            "has_severe_toxicity": scores.get("SEVERE_TOXICITY", 0) > 0.7,
        }

    return {
        "text": text,
        "toxicity_scores": {},
        "is_toxic": False,
        "has_severe_toxicity": False,
        "error": "Failed to analyze toxicity",
    }
