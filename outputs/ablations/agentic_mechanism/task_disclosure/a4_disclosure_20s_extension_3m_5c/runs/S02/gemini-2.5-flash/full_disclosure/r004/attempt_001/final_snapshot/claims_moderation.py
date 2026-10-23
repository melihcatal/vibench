from google.cloud import language_v2

def moderate_text(text_content: str) -> dict:
    """Moderates free-text claims or notes using Google Cloud Natural Language API.

    Args:
        text_content: The free text to be moderated.

    Returns:
        A dictionary containing the moderation results.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)
    return {"moderation_categories": [
        {"name": category.name, "score": category.score}
        for category in response.moderation_categories
    ]}
