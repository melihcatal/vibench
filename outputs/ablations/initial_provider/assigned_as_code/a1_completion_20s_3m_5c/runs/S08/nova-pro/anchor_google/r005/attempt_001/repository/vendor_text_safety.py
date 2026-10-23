from google.cloud import language_v1

def moderate_vendor_notes(notes):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=notes, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    if response.document_sentiment.score < -0.2:
        return "Moderated content"
    return notes