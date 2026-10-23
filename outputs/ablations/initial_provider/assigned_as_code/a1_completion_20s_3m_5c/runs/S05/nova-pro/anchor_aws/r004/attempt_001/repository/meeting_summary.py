from google.cloud import language
from google.cloud.language import enums

def summarize_text(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=enums.Document.Type.PLAIN_TEXT)
    analysis = client.analyze_entities(document)
    entities = [entity.name for entity in analysis.entities]
    return ' '.join(entities)