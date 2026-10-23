from google.cloud import language_v1


def check_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    if response.document_sentiment.score < -0.25:
        return "Unsafe content detected"
    else:
        return "Safe content"
