import google.cloud.language


def embed_text(text):
    client = google.cloud.language.LanguageServiceClient()
    document = google.cloud.language.types.Document(
        content=text, type=google.cloud.language.enums.Document.Type.PLAIN_TEXT
    )
    analysis = client.analyze_entities(document=document)
    entities = [entity.name for entity in analysis.entities]
    return " ".join(entities)
