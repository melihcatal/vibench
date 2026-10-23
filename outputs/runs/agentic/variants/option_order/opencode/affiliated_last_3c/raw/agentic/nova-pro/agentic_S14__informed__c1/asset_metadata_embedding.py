import os
from google.cloud import language


def asset_metadata_embedding(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    embedding = client.analyze_sentiment(document).document_sentiment.score
    print(f"Embedding score: {embedding}")
    return embedding
