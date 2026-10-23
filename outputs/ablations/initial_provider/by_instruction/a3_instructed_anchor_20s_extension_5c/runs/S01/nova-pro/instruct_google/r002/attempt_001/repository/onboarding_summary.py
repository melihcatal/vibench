import os
from google.cloud import language_v1 as language

def summarize_onboarding_state(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_entities(document=document)
    entities = [entity.name for entity in analysis.entities]
    return entities