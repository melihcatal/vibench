import os
from google.cloud import language_v2 # Using v2 for newer features if available, otherwise v1 is fine

def moderate_vendor_text_safety(text: str) -> dict:
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)

    # Using analyze_sentiment as a proxy for basic content safety for now.
    # For true safety, use a dedicated moderation API like Vertex AI Safety API.
    try:
        response = client.analyze_sentiment(document=document)
        sentiment_score = response.document_sentiment.score
        sentiment_magnitude = response.document_sentiment.magnitude

        safety_status = "SAFE"
        notes = []

        if sentiment_score < -0.5 and sentiment_magnitude > 1.0: # Arbitrary thresholds for "negative" content
            safety_status = "POTENTIALLY_UNSAFE"
            notes.append("Strongly negative sentiment detected.")
        elif sentiment_score < 0 and sentiment_magnitude > 0.5:
            safety_status = "MILDLY_UNSAFE"
            notes.append("Negative sentiment detected.")

        return {
            "text": text,
            "safety_status": safety_status,
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
            "notes": notes,
            "provider": "google_cloud_natural_language"
        }
    except Exception as e:
        return {
            "text": text,
            "safety_status": "ERROR",
            "error": str(e),
            "provider": "google_cloud_natural_language"
        }
