from google.cloud import language_v2 as language


def moderate_transcript(text: str):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    return client.moderate_text(request={"document": document})
