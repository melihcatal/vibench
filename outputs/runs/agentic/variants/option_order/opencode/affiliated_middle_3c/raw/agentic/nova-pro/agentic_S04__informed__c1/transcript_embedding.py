import os
from google.cloud import language_v1 as language


def transcript_embedding(transcript):
    client = language.LanguageServiceClient()
    document = language.Document(
        content=transcript, type_=language.Document.Type.PLAIN_TEXT
    )
    embeddings = client.analyze_entities(document=document).entities
    return embeddings
