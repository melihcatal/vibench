from google.cloud import language_v1 as language


def archive_summary(text: str):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={"document": document})
    return {"score": response.document_sentiment.score, "magnitude": response.document_sentiment.magnitude}
