from google.cloud import language_v1


def extract_fields_from_text(text: str):
    """
    Extracts structured fields (entities) from text using Google Cloud Natural Language API.
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    response = client.analyze_entities(document=document)

    entities = []
    for entity in response.entities:
        entities.append(
            {
                "name": entity.name,
                "type": language_v1.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            }
        )
    return entities
