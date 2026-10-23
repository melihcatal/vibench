from google.cloud import language_v1


def archive_summary(transcript):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=transcript, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    summary = client.analyze_sentiment(document).document_sentiment
    return summary.score, summary.magnitude
