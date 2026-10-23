from google.cloud import language_v1


def check_unsafe_content(text: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={"document": document})
    return {"unsafe": sentiment.document_sentiment.score < -0.5, "score": sentiment.document_sentiment.score}
