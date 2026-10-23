from google.cloud import language_v2

def moderate_transcript(text_content: str):
    """
    Moderates transcript text using Google Cloud Natural Language API.

    Args:
        text_content: The text content of the transcript to moderate.

    Returns:
        A list of content moderation annotations.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderate_text method to get content moderation scores
    response = client.moderate_text(document=document)
    return response.moderation_categories
