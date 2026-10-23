import os
from google.cloud import language_v1 as language

def archive_summary(transcript):
    client = language.LanguageServiceClient()
    document = language.Document(content=transcript, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document)
    return response.document_sentiment.text