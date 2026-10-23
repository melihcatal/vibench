import os
from google.cloud import language_v1 as language


def asset_metadata_embedding(metadata, text, config=None):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(document=document).entities
    embedding = [entity.name for entity in entities]
    return {"embedding": embedding}