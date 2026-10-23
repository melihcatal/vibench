from google.cloud import language_v1

def moderate_vendor_text(text_content: str):
    """
    Moderates vendor notes or memo fields using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    return response
