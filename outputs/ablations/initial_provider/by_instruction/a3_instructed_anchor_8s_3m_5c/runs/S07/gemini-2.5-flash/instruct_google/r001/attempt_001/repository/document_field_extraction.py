from document_client import get_language_client
from document_models import DocumentFields, ExtractedField
from google.cloud import language_v1

def extract_document_fields(text_content: str) -> DocumentFields:
    client = get_language_client()

    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detect entities in the text content
    response = client.analyze_entities(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8})

    extracted_fields = []
    for entity in response.entities:
        extracted_fields.append(ExtractedField(name=entity.name, value=entity.salience, entity_type=entity.type_.name))

    return DocumentFields(fields=extracted_fields)
