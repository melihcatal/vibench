from google.cloud import language_v1

def moderate_batch(texts: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages and returns per-message decisions using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()
    results = []
    for text_content in texts:
        document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
        # Using classify_text to simulate moderation categories, as direct content moderation is not a primary function
        # of the Natural Language API in the same way as specialized safety APIs.
        # For true content moderation, other Google Cloud services or specialized APIs would be used.
        try:
            response = client.classify_text(request={'document': document})
            categories = []
            for category in response.categories:
                categories.append({"name": category.name, "confidence": category.confidence})
            results.append({"text": text_content, "moderation_categories": categories, "provider": "Google Cloud Natural Language (Classify Text)"})
        except Exception as e:
            results.append({"text": text_content, "error": str(e), "provider": "Google Cloud Natural Language (Classify Text)"})
    return results
