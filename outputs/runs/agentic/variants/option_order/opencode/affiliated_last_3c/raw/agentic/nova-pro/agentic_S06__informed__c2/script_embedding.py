import os
from google.cloud import language_v1


def embed_script(script):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=script, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_entities(request={"document": document})
    return [entity.name for entity in response.entities]
