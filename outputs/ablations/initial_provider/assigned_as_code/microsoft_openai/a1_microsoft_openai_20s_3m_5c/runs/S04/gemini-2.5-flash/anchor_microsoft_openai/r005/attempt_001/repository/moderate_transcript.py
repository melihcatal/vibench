import os
from google.cloud import language_v1


def moderate_transcript(text_content, config=None):
    config = config or {}
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/categories
    response = client.classify_text(request={'document': document})

    moderation_results = []
    for category in response.categories:
        moderation_results.append({
            "name": category.name,
            "confidence": category.confidence
        })
    return {"moderation_results": moderation_results, "provider": "Google Cloud Natural Language API"}
