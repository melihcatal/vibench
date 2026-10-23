from google.cloud import language_v1
import os

def profile_moderation(text: str) -> dict:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS env var is set
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify content to detect categories that might indicate inappropriate content
    # Note: For more explicit moderation, consider Perspective API if available and suitable.
    # For general content classification, Natural Language API can give hints.
    response = client.classify_text(request={'document': document})

    moderation_results = {
        "categories": [{'name': category.name, 'confidence': category.confidence} for category in response.categories],
        "text": text
    }
    return moderation_results
