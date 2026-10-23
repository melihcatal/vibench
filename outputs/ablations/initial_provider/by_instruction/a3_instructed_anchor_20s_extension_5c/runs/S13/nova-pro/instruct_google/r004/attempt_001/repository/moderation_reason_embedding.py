import os
from google.cloud import language_v1

def embed_moderation_rationale(rationale):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=rationale, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    return response.document_sentiment.score

if __name__ == '__main__':
    sample_rationale = 'This is a moderation rationale to embed.'
    embedding = embed_moderation_rationale(sample_rationale)
    print(f'Embedding: {embedding}')
