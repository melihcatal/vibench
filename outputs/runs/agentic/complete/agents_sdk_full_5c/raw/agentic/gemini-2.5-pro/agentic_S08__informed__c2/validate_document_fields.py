
from azure.ai.documentintelligence.models import AnalyzeResult
from typing import List, Dict, Any

def validate_document_fields(
    result: AnalyzeResult, 
    required_fields: List[str],
    confidence_threshold: float = 0.8
) -> Dict[str, Any]:
    """
    Validates required fields and their confidence scores from an AnalyzeResult.

    Args:
        result: The AnalyzeResult object from Azure Document Intelligence.
        required_fields: A list of field names that must be present.
        confidence_threshold: The minimum confidence score for a field to be valid.

    Returns:
        A dictionary containing validation status and a list of errors.
    """
    errors = []
    is_valid = True

    if not result.documents:
        return {"is_valid": False, "errors": ["No document was analyzed."]}

    doc = result.documents[0]
    
    for field_name in required_fields:
        field = doc.fields.get(field_name)
        if not field:
            errors.append(f"Missing required field: {field_name}")
            is_valid = False
            continue
        
        # Confidence is a provider-specific signal from Azure
        if field.confidence < confidence_threshold:
            errors.append(
                f"Field '{field_name}' has low confidence: {field.confidence:.2f}"
            )
            is_valid = False

    return {"is_valid": is_valid, "errors": errors}
