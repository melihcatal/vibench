from google.cloud import language_v2

def check_unsafe_content(text_content: str):
    """
    Checks live transcript text for unsafe content using Google Cloud Language AI.

    Args:
        text_content: The text to be checked for unsafe content.

    Returns:
        A ModerateTextResponse object containing the safety attributes.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    return response
