import os
from google.cloud import language_v1 as language

def archive_summary(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(request={'document': document}).document_sentiment.text
    return summary