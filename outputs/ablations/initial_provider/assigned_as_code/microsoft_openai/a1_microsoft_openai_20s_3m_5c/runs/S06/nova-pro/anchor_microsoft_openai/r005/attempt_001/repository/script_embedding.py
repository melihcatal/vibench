import google.cloud.language as language

def embed_text(text):
    client = language.Client()
    document = client.document_from_text(text)
    analysis = document.analyze_entities()
    return [entity.name for entity in analysis.entities]