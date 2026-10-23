import os
from google.cloud import language_v1

def redact_unsafe(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    if response.document_sentiment.score < -0.5:
        return '[REDACTED]'
    return text