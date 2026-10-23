from document_client import DocumentClient
from document_models import FieldExtractionRequest, FieldExtractionResponse
import logging

logger = logging.getLogger(__name__)

def extract_fields(request: FieldExtractionRequest) -> FieldExtractionResponse:
    client = DocumentClient()
    comprehend_client = client.comprehend_client

    # Detect dominant language
    dominant_language_response = comprehend_client.detect_dominant_language(
        Text=request.document_text
    )
    dominant_language_code = dominant_language_response['Languages'][0]['LanguageCode']

    # Use Comprehend to detect entities in the text
    entities_response = comprehend_client.detect_entities(
        Text=request.document_text,
        LanguageCode=dominant_language_code
    )

    extracted_fields = {}
    for entity in entities_response['Entities']:
        entity_type = entity['Type']
        entity_text = entity['Text']
        if entity_type not in extracted_fields:
            extracted_fields[entity_type] = []
        extracted_fields[entity_type].append(entity_text)

    # For more specific field extraction, a custom Comprehend entity recognizer or rule-based parsing
    # would be implemented here, potentially mapping generic entities to specific document fields.

    return FieldExtractionResponse(extracted_fields=extracted_fields, raw_response=entities_response)
