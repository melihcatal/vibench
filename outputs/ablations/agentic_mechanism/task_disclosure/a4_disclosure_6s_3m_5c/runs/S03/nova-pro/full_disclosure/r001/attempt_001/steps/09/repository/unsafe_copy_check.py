import os
from google.cloud import language_v2

def check_unsafe_content(text):
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    client = language_v2.LanguageServiceClient(api_key=api_key)
    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    sentiment = response.document_sentiment
    if sentiment.score < -0.5:
        return True
    else:
        return False