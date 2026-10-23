import os
from google.cloud import language_v1


def message_safety(message):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=message, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    safety = client.analyze_sentiment(document)
    return safety.document_sentiment.score > -0.5
