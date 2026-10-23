from google.cloud import language_v1

from document_models import TextResponse


def extract_document_fields(text_response: TextResponse) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_response.text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    entities = client.analyze_entities(request={"document": document}).entities
    return {entity.name: entity.type_.name for entity in entities}
