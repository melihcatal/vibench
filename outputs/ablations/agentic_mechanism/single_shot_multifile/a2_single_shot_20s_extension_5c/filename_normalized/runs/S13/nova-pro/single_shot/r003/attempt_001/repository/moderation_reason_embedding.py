import os
from google.cloud import language_v1

def moderation_reason_embedding(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(request={'document': document})
    return [entity.salience for entity in response.entities]
