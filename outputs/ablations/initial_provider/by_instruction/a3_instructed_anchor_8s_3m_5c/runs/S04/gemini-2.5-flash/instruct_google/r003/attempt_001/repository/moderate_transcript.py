from google.cloud import language_v1

def moderate_text(text: str):
    """Moderates transcript text using Google Cloud Natural Language API to classify content.

    Args:
        text: The text to moderate.

    Returns:
        A list of content categories and their confidence scores.
    """
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Classify content to detect categories
    response = client.classify_text(request={'document': document})

    categories = []
    for category in response.categories:
        categories.append({
            "name": category.name,
            "confidence": category.confidence
        })
    
    print(f"Moderation results: {categories}")
    return categories
