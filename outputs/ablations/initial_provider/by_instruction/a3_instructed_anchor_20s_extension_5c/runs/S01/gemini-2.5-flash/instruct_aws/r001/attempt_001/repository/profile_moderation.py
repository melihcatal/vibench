from google.cloud import language_v1
import os

def profile_moderation(text_content):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type=language_v1.Document.Type.PLAIN_TEXT
    )

    # Classify content to detect categories that might be undesirable
    response = client.classify_text(request={'document': document})

    # For simplicity, we'll just return the categories and their confidence scores.
    # In a real moderation scenario, you'd have rules to flag certain categories.
    moderation_results = []
    for category in response.categories:
        moderation_results.append({
            "name": category.name,
            "confidence": category.confidence
        })

    return moderation_results
