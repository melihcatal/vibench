from google.cloud import language

def embed_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type=language.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_entities(document=document)
    return [entity.name for entity in analysis.entities]