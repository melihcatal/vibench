import os
from typing import Dict, Any, List, Tuple
from document_models import DocumentExtraction, parse_textract_expense_response


def validate_document_fields(
    extracted_data: Dict[str, Any],
    required_fields: List[str] = None,
    min_confidence: float = 0.7,
) -> Dict[str, Any]:
    """
    Validate required structured fields and confidence scores from extracted document data.

    Args:
        extracted_data: Extracted data from document
        required_fields: List of required field names
        min_confidence: Minimum confidence threshold for validation

    Returns:
        Validation results with status and details
    """
    if required_fields is None:
        required_fields = ["vendor", "date", "total"]

    # Parse data based on format
    if "ExpenseDocuments" in extracted_data:
        extraction = parse_textract_expense_response(extracted_data)
        fields_map = {
            "vendor": extraction.vendor,
            "merchant": extraction.merchant,
            "date": extraction.date,
            "total": extraction.total,
            "tax": extraction.tax,
        }
    else:
        # Map from extracted data dictionary
        fields_map = {}
        for field in ["vendor", "merchant", "date", "total", "tax"]:
            value = extracted_data.get(field)
            confidence = extracted_data.get(f"{field}_confidence", 0.0)
            if value is not None:
                from document_models import ExpenseField

                fields_map[field] = ExpenseField(
                    field_type=field, value=value, confidence=confidence
                )

    # Perform validation
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "field_details": {},
        "overall_confidence": 0.0,
        "validation_provider": "Amazon Textract AnalyzeExpense",
    }

    total_confidence = 0.0
    field_count = 0

    for field_name in required_fields:
        field = fields_map.get(field_name)

        if field is None:
            validation_results["missing_fields"].append(field_name)
            validation_results["is_valid"] = False
            validation_results["field_details"][field_name] = {
                "present": False,
                "confidence": 0.0,
                "value": None,
            }
        else:
            field_detail = {
                "present": True,
                "confidence": field.confidence,
                "value": field.value,
            }

            if field.confidence < min_confidence:
                validation_results["low_confidence_fields"].append(field_name)
                validation_results["is_valid"] = False
                field_detail["confidence_issue"] = True
            else:
                field_detail["confidence_issue"] = False

            validation_results["field_details"][field_name] = field_detail

            total_confidence += field.confidence
            field_count += 1

    # Calculate overall confidence
    if field_count > 0:
        validation_results["overall_confidence"] = total_confidence / field_count

    # Validate line items
    if "line_items" in extracted_data or "items" in extracted_data:
        items_key = "line_items" if "line_items" in extracted_data else "items"
        items = extracted_data.get(items_key, [])
        validation_results["item_count"] = len(items)

        if len(items) == 0:
            validation_results["item_warning"] = "No line items found"

    # Add AWS-specific validation info
    validation_results["aws_service"] = "textract.analyze_expense"
    validation_results["min_confidence_threshold"] = min_confidence

    return validation_results
