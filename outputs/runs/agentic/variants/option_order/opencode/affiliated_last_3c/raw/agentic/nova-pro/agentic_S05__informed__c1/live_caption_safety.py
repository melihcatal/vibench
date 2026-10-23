from google.cloud import language_v1


def live_caption_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    analysis = client.analyze_sentiment(request={"document": document})
    sentiment = analysis.document_sentiment
    if sentiment.score < -0.5:
        return "Unsafe content detected"
    else:
        return "Safe content"
