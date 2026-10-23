import os
from google.cloud import language_v1


def check_safety(script):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=script, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(request={"document": document})
    return response.document_sentiment.score >= -0.5
