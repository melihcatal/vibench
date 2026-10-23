from google.cloud import language_v1


def record_text_safety(text):
    client = language_v1.LanguageServiceClient()
    doc = language_v1.Document(content=text or "", type_=language_v1.Document.Type.PLAIN_TEXT)
    return client.moderate_text(document=doc)
