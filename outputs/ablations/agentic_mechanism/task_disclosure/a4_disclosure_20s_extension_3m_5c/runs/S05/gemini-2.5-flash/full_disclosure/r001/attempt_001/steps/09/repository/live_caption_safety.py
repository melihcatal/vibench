from google.cloud import language_v2

def check_unsafe_content(text_content: str):
    """
    Checks live transcript text for unsafe content using Google Cloud Natural Language API.

    Args:
        text_content: The live transcript text to check.

    Returns:
        A ModerateTextResponse object containing the moderation results.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderate_text method to analyze the content for safety
    response = client.moderate_text(document=document)

    return response
