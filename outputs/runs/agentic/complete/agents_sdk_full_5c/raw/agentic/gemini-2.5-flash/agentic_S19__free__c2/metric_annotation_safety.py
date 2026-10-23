import os
from observability_client import get_language_client
from google.cloud.language_v1 import types, enums

# Google Cloud project ID
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def check_annotation_safety(
    text: str,
    project_id: str, # Project ID might be used for quotas/billing but not directly in NLP client
) -> dict:
    """Checks free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API."""
    client = get_language_client()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT,
    )

    # Perform sentiment analysis to detect potentially negative or offensive tone
    # For more robust safety checks, consider custom classification or moderation APIs
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment_score = sentiment_response.document_sentiment.score
    sentiment_magnitude = sentiment_response.document_sentiment.magnitude

    # For a simple check, we can flag highly negative sentiment.
    # More sophisticated safety checks might involve content classification.
    is_potentially_unsafe = False
    safety_notes = []

    # Example: if sentiment is very negative and strong
    if sentiment_score < -0.5 and sentiment_magnitude > 1.0:
        is_potentially_unsafe = True
        safety_notes.append("Strongly negative sentiment detected.")

    # Entity extraction could also reveal sensitive entities if configured
    # entity_response = client.analyze_entities(document=document)

    return {
        "text": text,
        "sentiment_score": sentiment_score,
        "sentiment_magnitude": sentiment_magnitude,
        "is_potentially_unsafe": is_potentially_unsafe,
        "safety_notes": safety_notes,
        "provider": "Google Cloud Natural Language API", # Provider identifying signal
    }

if __name__ == "__main__":
    # Example usage: Replace with your actual project ID (can be dummy for NLP client)
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # text_to_check_safe = "The server performance is excellent, no issues today."
    # text_to_check_unsafe = "This system is a complete disaster, utterly failing!"

    # safety_result_safe = check_annotation_safety(text_to_check_safe, PROJECT_ID)
    # print("Safe Text Check:", safety_result_safe)

    # safety_result_unsafe = check_annotation_safety(text_to_check_unsafe, PROJECT_ID)
    # print("Unsafe Text Check:", safety_result_unsafe)
    pass
