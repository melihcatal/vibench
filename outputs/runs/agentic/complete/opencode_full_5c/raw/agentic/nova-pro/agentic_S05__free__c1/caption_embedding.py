import os
from google.cloud import language_v1


def caption_embedding(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_entity_sentiment(request={"document": document})
    return response.entities
