import google.cloud.language


def check_safety(text):
    client = google.cloud.language.LanguageServiceClient()
    document = google.cloud.language.types.Document(
        content=text, type=google.cloud.language.enums.Document.Type.PLAIN_TEXT
    )
    analysis = client.analyze_sentiment(document=document)
    return analysis.document_sentiment.score >= -0.2
