from google.cloud import language_v2

def check_unsafe_content(text_content: str) -> bool:
    """Checks message payload text for unsafe content using Google Cloud Language AI.

    Args:
        text_content: The text content of the message payload.

    Returns:
        True if the content is safe, False otherwise.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT)

    response = client.moderate_text(document=document)

    # If any category has a moderation score above a certain threshold (e.g., 0.5), consider it unsafe.
    # The actual threshold might need to be adjusted based on requirements.
    for category in response.moderation_categories:
        if category.score > 0.5:
            return False
    return True
