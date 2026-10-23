from google.cloud import language_v2

def check_unsafe_text(text_content: str):
    """
    Checks free-text metric labels or annotations for unsafe text using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderateText method for content moderation
    response = client.moderate_text(document=document)

    return response.moderation_categories
