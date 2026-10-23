import os
from google.cloud import language_v1

def create_safety_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    return language_v1.LanguageServiceClient()

def moderate_text(client, text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    return response.document_sentiment.score
