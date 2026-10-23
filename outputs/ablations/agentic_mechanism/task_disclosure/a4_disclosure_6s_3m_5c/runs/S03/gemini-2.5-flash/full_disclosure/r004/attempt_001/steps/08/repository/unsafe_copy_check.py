import google.cloud.language_v2 as language_v2

def check_unsafe_content(text_content: str):
    """Checks localized copy for unsafe content using Google Cloud Language AI.

    Args:
        text_content: The text content to check.

    Returns:
        A ModerateTextResponse object containing content moderation results.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )
    response = client.moderate_text(document=document)
    return response

