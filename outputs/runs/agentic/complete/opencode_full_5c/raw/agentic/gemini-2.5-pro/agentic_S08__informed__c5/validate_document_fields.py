from typing import Dict, Any, List

MIN_CONFIDENCE_SCORE = 0.8


def validate_document_fields(analysis_result: Any) -> Dict[str, List[str]]:
    """
    Validates the extracted fields from an Azure Document Intelligence result.
    """
    errors = {"missing_fields": [], "low_confidence": []}

    if not analysis_result.documents:
        errors["missing_fields"].append("document")
        return errors

    doc = analysis_result.documents[0]

    required_fields = []
    if doc.doc_type == "prebuilt-invoice":
        required_fields = ["VendorName", "InvoiceDate", "InvoiceTotal"]
    elif doc.doc_type == "prebuilt-receipt":
        required_fields = ["MerchantName", "TransactionDate", "Total"]

    for field_name in required_fields:
        field = doc.fields.get(field_name)
        if not field:
            errors["missing_fields"].append(field_name)
        elif field.confidence < MIN_CONFIDENCE_SCORE:
            errors["low_confidence"].append(
                f"{field_name} (confidence: {field.confidence:.2f})"
            )

    return errors
