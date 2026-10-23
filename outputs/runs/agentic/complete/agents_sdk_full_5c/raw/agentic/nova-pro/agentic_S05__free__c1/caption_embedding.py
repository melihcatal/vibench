import os
from google.cloud import language_v1 as language

client = language.LanguageServiceClient()

def embed_text(text):
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    embedding = client.analyze_entity_sentiment(request={'document': document}).document_sentiment.score
    return embedding