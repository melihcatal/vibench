from google.cloud import language_v1

def moderate_text(text_content: str) -> dict:
    """
    Moderates vendor notes or memo fields using Google Cloud Natural Language API.

    Args:
        text_content: The text content to moderate.

    Returns:
        A dictionary containing the moderation results.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Available categories: https://cloud.google.com/natural-language/docs/moderating-content
    response = client.moderate_text(document=document)

    moderation_results = []
    for category_filter in response.moderation_categories:
        moderation_results.append(
            {"name": category_filter.name, "confidence": category_filter.confidence}
        )
    return {"moderation_results": moderation_results}
