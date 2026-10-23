import os
import re
from google.cloud import language_v1 as language

def check_safety(text):
    client = language.LanguageServiceClient(os.getenv('GOOGLE_CLOUD_LANGUAGE_API_KEY'))
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_sentiment(document=document)
    sentiment = analysis.document_sentiment
    if sentiment.score < -0.5:
        return 'Unsafe'
    return 'Safe'