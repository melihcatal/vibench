from google.cloud import language_v2

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text before account activation using Google Cloud Natural Language API.
    """
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)

    # Use the moderateText method for content moderation
    response = client.moderate_text(document=document)

    # The response contains a list of moderation categories and their confidence scores.
    # You can process this response to determine if the content is acceptable.
    # For simplicity, this example returns the raw response.
    return {"moderation_result": response.moderation_categories}

