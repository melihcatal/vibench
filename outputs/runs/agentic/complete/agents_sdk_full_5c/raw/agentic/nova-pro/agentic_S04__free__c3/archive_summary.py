import os
from google.cloud import language

def archive_summary(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(document).document_sentiment.score
    return summary