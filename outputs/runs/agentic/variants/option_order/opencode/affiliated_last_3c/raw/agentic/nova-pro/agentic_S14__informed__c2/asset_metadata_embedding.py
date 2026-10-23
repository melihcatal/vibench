import os
from google.cloud import language_v1 as language


def asset_metadata_embedding(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(document=document).entities

    embeddings = [entity.salience for entity in entities]

    print(f"Embeddings: {embeddings}")
    return embeddings
