from google.cloud import language_v1


def is_safe_message(text: str) -> bool:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment
    return sentiment.score >= -0.5
