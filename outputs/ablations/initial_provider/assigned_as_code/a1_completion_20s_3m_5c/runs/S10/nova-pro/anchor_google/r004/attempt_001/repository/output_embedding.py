import os
import google.auth
from google.cloud import language_v1 as language


def embed_output(text):
    credentials, _ = google.auth.default()
    language_client = language.LanguageServiceClient(credentials=credentials)
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    entities = language_client.analyze_entities(document=document).entities
    return [entity.name for entity in entities]