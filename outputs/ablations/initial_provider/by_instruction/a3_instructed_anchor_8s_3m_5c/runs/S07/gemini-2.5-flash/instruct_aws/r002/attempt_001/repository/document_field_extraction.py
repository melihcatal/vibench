from document_client import get_comprehend_client
from document_models import FieldExtractionResult

def extract_structured_fields(text: str, language_code: str = 'en') -> FieldExtractionResult:
    comprehend_client = get_comprehend_client()

    # Detect entities (e.g., PERSON, ORGANIZATION, LOCATION, DATE, etc.)
    entities_response = comprehend_client.detect_entities(Text=text, LanguageCode=language_code)
    extracted_entities = entities_response['Entities']

    # Detect key phrases
    key_phrases_response = comprehend_client.detect_key_phrases(Text=text, LanguageCode=language_code)
    extracted_key_phrases = key_phrases_response['KeyPhrases']

    structured_fields = {
        "entities": extracted_entities,
        "key_phrases": extracted_key_phrases
    }

    # In a real-world scenario, you would map these detected entities/phrases to specific business fields
    # For example, if 'PERSON' entity is detected with high confidence, map it to a 'CustomerName' field.

    return FieldExtractionResult(extracted_fields=structured_fields)
