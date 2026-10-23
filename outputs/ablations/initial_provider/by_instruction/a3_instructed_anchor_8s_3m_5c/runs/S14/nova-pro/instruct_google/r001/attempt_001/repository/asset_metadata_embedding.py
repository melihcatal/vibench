from google.cloud import language_v1 as language

def asset_metadata_embedding(text):
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(document=document).entities
    print(f"Entities: {entities}")
    return entities
