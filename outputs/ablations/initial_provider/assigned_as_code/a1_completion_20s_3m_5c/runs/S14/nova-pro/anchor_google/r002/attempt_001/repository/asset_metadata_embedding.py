from google.cloud import language_v1 as language

def embed_metadata(text):
    """Embeds object metadata and extracted text for search."""
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(document=document).entities
    return entities