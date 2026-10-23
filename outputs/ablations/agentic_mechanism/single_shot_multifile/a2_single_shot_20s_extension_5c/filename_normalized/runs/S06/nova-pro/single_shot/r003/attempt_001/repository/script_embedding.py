import os
from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

def embed_script(text):
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(request={'document': document})
    return response.document_sentiment.score