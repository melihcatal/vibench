from google.cloud import language_v1

def check_content_safety(text: str) -> list[dict]:
    """Checks extracted document text for unsafe content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classifying text to infer safety. This is a proxy for safety and not a direct safety API.
    # A more robust solution might involve specific safety APIs if available.
    response = client.classify_text(request={'document': document})
    
    categories = []
    for category in response.categories:
        categories.append({
            "name": category.name,
            "confidence": category.confidence
        })
    return categories
