from google.cloud import language_v2

def moderate_text(text_content: str):
    """Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API."""

    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=text_content,
        type_=language_v2.Document.Type.PLAIN_TEXT,
    )

    response = client.moderate_text(document=document)
    return response
