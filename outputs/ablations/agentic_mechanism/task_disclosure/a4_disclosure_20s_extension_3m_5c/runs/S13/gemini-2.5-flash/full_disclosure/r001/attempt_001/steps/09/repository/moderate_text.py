from google.cloud import language_v2

def moderate_text_content(text_content: str):
    """Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API."""
    client = language_v2.LanguageServiceClient()
    document = language_v2.Document(
        content=text_content, type_=language_v2.Document.Type.PLAIN_TEXT
    )
    
    # Google Cloud Natural Language API's moderateText method
    response = client.moderate_text(document=document)

    return response.moderation_categories
