import os
from translation_client import TranslationClient
from translation_models import QualitySummaryRequest
from google.cloud import language_v2 as language

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def summarize_quality_issues(request: QualitySummaryRequest) -> dict:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    client = TranslationClient(project_id=PROJECT_ID)
    sentiment = client.analyze_sentiment(request.text, request.language)

    summary = {
        "score": sentiment.score,
        "magnitude": sentiment.magnitude,
        "overall_sentiment_description": "Positive"
        if sentiment.score > 0.25
        else ("Negative" if sentiment.score < -0.25 else "Neutral"),
        "issues_detected": [],
    }

    if sentiment.score < -0.25:  # Arbitrary threshold for negative sentiment
        summary["issues_detected"].append("Negative sentiment detected in translation.")

    # Further analysis could be added here, e.g., entity extraction for specific terms

    return summary
