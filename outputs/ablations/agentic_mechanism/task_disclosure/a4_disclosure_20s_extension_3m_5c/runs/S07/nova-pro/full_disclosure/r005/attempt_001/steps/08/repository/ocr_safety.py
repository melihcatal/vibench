import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums

def check_safety(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    if analysis.document_sentiment.score < -0.5:
        return 'Unsafe'
    else:
        return 'Safe'