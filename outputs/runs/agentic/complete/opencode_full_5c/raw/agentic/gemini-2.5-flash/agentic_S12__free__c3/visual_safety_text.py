from google.cloud import language_v1
import os


def check_text_safety(text: str):
    """
    Checks generated visual labels for unsafe text using Google Cloud Natural Language AI.
    Provider: Google Cloud Natural Language AI
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Perform content moderation
    # Note: `moderate_text` is more suitable for general safety, `analyze_sentiment` for sentiment.
    # We'll use `moderate_text` for "safety".
    response = client.moderate_text(document=document)

    safety_scores = {}
    if response.moderation_categories:
        for category in response.moderation_categories:
            safety_scores[category.name] = category.score

    return safety_scores
