from google.cloud import language_v2

def check_safety(text_content: str):
    """Checks text payloads for unsafe content using Google Cloud's Language AI."""
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )

    # Use the moderateText API for content safety
    response = client.moderate_text(document=document)

    # The response contains categories and their confidence scores
    # You can process these categories to determine if the content is unsafe
    return response.moderation_categories
