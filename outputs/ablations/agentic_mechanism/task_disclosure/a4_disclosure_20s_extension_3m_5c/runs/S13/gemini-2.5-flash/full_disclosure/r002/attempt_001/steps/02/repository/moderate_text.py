from google.cloud import language_v1

def moderate_text(text: str):
    """Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.moderate_text(document=document)
    return response
