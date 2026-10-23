import os
from google.cloud import language_v1

def moderation_summary(texts):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=texts, type_=language_v1.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(document=document).document_sentiment
    return summary