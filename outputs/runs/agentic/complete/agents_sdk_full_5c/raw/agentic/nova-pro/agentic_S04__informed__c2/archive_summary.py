import os
from google.cloud import language_v1 as language

client = language.LanguageServiceClient()

def archive_summary(transcript_text):
    document = language.Document(content=transcript_text, type_=language.Document.Type.PLAIN_TEXT)
    summary = client.analyze_sentiment(request={'document': document}).document_sentiment.text
    return summary