import os
from google.cloud import language_v1 as language

client = language.LanguageServiceClient()

def summarize_text(text):
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(request={'document': document}).document_sentiment.score
    return summary