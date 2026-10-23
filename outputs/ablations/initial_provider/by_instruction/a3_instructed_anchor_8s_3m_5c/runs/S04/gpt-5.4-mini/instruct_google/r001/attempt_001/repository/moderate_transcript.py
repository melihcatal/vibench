from google.cloud import language_v1


def moderate_transcript(text: str):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    return {"text": text, "score": sentiment.document_sentiment.score, "magnitude": sentiment.document_sentiment.magnitude}
