import os
import json
from google.cloud import language_v1

def check_unsafe_content(text):
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment
    if sentiment.score < -0.5:
        return True
    else:
        return False