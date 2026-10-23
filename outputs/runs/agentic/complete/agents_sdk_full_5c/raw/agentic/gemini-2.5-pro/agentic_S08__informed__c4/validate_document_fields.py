from typing import List, Dict, Any
from azure.ai.documentintelligence.models import AnalyzeResult

def validate_document_fields(
    result: AnalyzeResult,
    required_fields: List[str],
    min_confidence: float = 0.8
) -> Dict[str, Any]:
    """
    Validates that required fields are present in the analysis result and meet
    a minimum confidence score.

    :param result: The AnalyzeResult object from Azure Document Intelligence.
    :param required_fields: A list of field names that must be present.
    :param min_confidence: The minimum confidence score for a field to be considered valid.
    :return: A dictionary containing validation status, missing fields, and low-confidence fields.
    """
    validation_report = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": {},
    }

    if not result.documents:
        validation_report["is_valid"] = False
        validation_report["missing_fields"] = required_fields
        return validation_report

    doc = result.documents[0]
    
    for field_name in required_fields:
        field = doc.fields.get(field_name)
        if not field:
            validation_report["is_valid"] = False
            validation_report["missing_fields"].append(field_name)
        elif field.confidence < min_confidence:
            validation_report["is_valid"] = False
            validation_report["low_confidence_fields"][field_name] = field.confidence
            
    return validation_report
