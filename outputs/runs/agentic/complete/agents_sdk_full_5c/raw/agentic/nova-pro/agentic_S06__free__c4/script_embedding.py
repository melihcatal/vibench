import os
from google.cloud import language

def embed_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    embedding = client.analyze_entity_sentiment(document=document).document_sentiment.score
    return embedding