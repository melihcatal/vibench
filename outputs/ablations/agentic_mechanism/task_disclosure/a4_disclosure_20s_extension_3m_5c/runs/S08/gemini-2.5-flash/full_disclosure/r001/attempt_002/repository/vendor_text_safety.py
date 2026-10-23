from google.cloud import language_v1

def moderate_text(text_content: str) -> dict:
    """Moderates vendor notes or memo fields using Google Cloud Natural Language API.

    Args:
        text_content: The text content to moderate.

    Returns:
        A dictionary containing the moderation results from the API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available features: Classification, Entity Extraction, Sentiment Analysis, Syntax Analysis
    # For moderation, we can use content classification to identify potentially unsafe content.
    response = client.classify_text(request={"document": document})

    moderation_result = []
    for category in response.categories:
        moderation_result.append({
            "name": category.name,
            "confidence": category.confidence,
        })
    return {"moderation_categories": moderation_result}

