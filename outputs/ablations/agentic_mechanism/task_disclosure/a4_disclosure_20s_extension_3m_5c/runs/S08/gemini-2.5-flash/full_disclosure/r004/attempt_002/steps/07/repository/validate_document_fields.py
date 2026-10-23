from google.cloud import documentai_v1beta3 as documentai

def validate_document_fields(document_response: documentai.Document, required_fields: list, confidence_threshold: float = 0.9) -> dict:
    """
    Validates required structured fields and their confidence scores from a Document AI response.

    Args:
        document_response: The Document AI Document object containing extracted entities.
        required_fields: A list of strings, where each string is the type of a required field.
        confidence_threshold: The minimum confidence score required for a field to be considered valid.

    Returns:
        A dictionary with validation results, including missing fields, low confidence fields,
        and a boolean indicating overall validation success.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "validated_fields": {}
    }

    if not document_response.entities:
        validation_results["is_valid"] = False
        validation_results["missing_fields"].extend(required_fields)
        return validation_results

    extracted_fields = {entity.type: entity for entity in document_response.entities}

    for field_name in required_fields:
        if field_name not in extracted_fields:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field_name)
        else:
            entity = extracted_fields[field_name]
            # Document AI confidence is a float from 0 to 1
            if hasattr(entity, 'confidence') and entity.confidence < confidence_threshold:
                validation_results["is_valid"] = False
                validation_results["low_confidence_fields"].append({
                    "field": field_name,
                    "confidence": entity.confidence,
                    "value": entity.text
                })
            validation_results["validated_fields"][field_name] = {
                "value": entity.text,
                "confidence": entity.confidence
            }
            
    return validation_results
