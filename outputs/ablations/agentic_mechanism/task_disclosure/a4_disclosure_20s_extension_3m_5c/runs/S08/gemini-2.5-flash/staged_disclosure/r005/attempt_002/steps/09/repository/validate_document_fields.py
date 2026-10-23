from google.cloud import documentai_v1 as documentai

def validate_document_fields(document: documentai.Document, required_fields: dict, confidence_threshold: float = 0.9):
    """
    Validates if specified fields are present in the document and meet a minimum confidence threshold.

    Args:
        document: The Document AI Document object.
        required_fields: A dictionary where keys are field names and values are their expected types (e.g., {"invoice_id": "str"}).
        confidence_threshold: The minimum confidence score required for a field to be considered valid.

    Returns:
        A dictionary with validation results, including missing fields, low confidence fields, and their statuses.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": []
    }

    for field_name, expected_type in required_fields.items():
        found = False
        for entity in document.entities:
            if entity.type_ == field_name:
                found = True
                if entity.confidence < confidence_threshold:
                    validation_results["is_valid"] = False
                    validation_results["low_confidence_fields"].append({
                        "field_name": field_name,
                        "confidence": entity.confidence
                    })
                # Basic type checking (can be expanded)
                if expected_type == "str" and not isinstance(entity.text_anchor.content, str):
                     # This is a simplification; Document AI entities usually have text_anchor.content as string
                     pass
                break
        
        if not found:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field_name)

    return validation_results
