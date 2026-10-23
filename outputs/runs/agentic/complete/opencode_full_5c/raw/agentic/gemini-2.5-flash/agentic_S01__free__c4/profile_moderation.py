from google.cloud import language_v1
from google.cloud.language_v1 import Document, enums
import os


def moderate_profile_text(text: str) -> dict:
    # Google Cloud Natural Language API client will automatically pick up credentials
    # from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS or default service account)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print(
            "Warning: GOOGLE_CLOUD_PROJECT_ID not set. Natural Language client will attempt to infer project."
        )

    client = language_v1.LanguageServiceClient(project=project_id)

    document = Document(content=text, type=enums.Document.Type.PLAIN_TEXT)

    try:
        # Analyze sentiment as a basic form of moderation (e.g., detect very negative sentiment)
        sentiment = client.analyze_sentiment(document=document).document_sentiment

        # You could also use client.classify_text for content categorization
        # or client.annotate_text for a broader range of features including entities, syntax, etc.

        return {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude,
            "moderation_status": "flagged"
            if sentiment.score < -0.5 or sentiment.magnitude > 2.0
            else "clean",
        }
    except Exception as e:
        raise RuntimeError(f"Failed to moderate profile text: {e}")
