import os
from google.cloud import language_v1

client = language_v1.LanguageServiceClient()


def message_safety(text):
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    entities = client.analyze_entities(request={"document": document}).entities
    for entity in entities:
        if entity.salience > 0.5 and entity.name in ["violence", "hate"]:
            return False
    return True
