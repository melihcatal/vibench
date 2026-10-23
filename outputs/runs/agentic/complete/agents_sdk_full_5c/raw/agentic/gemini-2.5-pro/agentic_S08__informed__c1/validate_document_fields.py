from typing import Any, Dict, List
from google.cloud.documentai_v1.types import Document

MIN_CONFIDENCE_THRESHOLD = 0.85

def validate_document_fields(
    doc_ai_document: Document, required_fields: List[str]
) -> bool:
    """
    Validates the presence and confidence of required fields from a
    Google Document AI processor result.
    
    Args:
        doc_ai_document: The Document object from a Google Document AI response.
        required_fields: A list of field types that must be present.
    
    Returns:
        True if all required fields are present and meet the confidence
        threshold, False otherwise.
    """
    if not doc_ai_document or not doc_ai_document.entities:
        return False
        
    found_fields = {entity.type_: entity for entity in doc_ai_document.entities}

    for field_name in required_fields:
        if field_name not in found_fields:
            return False  # Field is missing

        entity = found_fields[field_name]
        if entity.confidence < MIN_CONFIDENCE_THRESHOLD:
            return False  # Field confidence is too low
            
    return True
