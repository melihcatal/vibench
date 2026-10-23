from typing import Dict, Any, Tuple
from document_models import InvoiceFields, ReceiptFields


def validate_document_fields(
    extracted_data: Dict[str, Any], document_type: str
) -> Tuple[bool, Dict[str, Any]]:
    validation_result = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "errors": [],
    }

    try:
        if document_type == "invoice":
            invoice = InvoiceFields(**extracted_data)
            if not invoice.vendor:
                validation_result["missing_fields"].append("vendor")
                validation_result["is_valid"] = False
            if not invoice.date:
                validation_result["missing_fields"].append("date")
                validation_result["is_valid"] = False
            if invoice.total is None:
                validation_result["missing_fields"].append("total")
                validation_result["is_valid"] = False
            if invoice.confidence and invoice.confidence < 0.7:
                validation_result["low_confidence_fields"].append("overall")

        elif document_type == "receipt":
            receipt = ReceiptFields(**extracted_data)
            if not receipt.merchant:
                validation_result["missing_fields"].append("merchant")
                validation_result["is_valid"] = False
            if receipt.total is None:
                validation_result["missing_fields"].append("total")
                validation_result["is_valid"] = False
            if receipt.confidence and receipt.confidence < 0.7:
                validation_result["low_confidence_fields"].append("overall")

        else:
            raise ValueError(f"Unsupported document type: {document_type}")

    except Exception as e:
        validation_result["is_valid"] = False
        validation_result["errors"].append(str(e))

    return validation_result["is_valid"], validation_result
