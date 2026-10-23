import os
from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

def summarize_moderation_decisions(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(document=document).document_sentiment.text
    return summary