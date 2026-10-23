from google.cloud import language
from google.cloud.language import enums

def embed_text(text):
    client = language.LanguageServiceClient()
    document = language.types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_entities(document=document)
    entities = [entity.name for entity in analysis.entities]
    return ' '.join(entities[:5])