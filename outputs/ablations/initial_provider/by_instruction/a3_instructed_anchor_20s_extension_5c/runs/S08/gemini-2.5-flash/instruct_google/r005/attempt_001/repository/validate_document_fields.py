from typing import List, Union
from document_models import ExtractedInvoiceFields, ExtractedReceiptFields, DocumentFieldValidation

def validate_document_fields(
    extracted_document: Union[ExtractedInvoiceFields, ExtractedReceiptFields]
) -> List[DocumentFieldValidation]:
    """Validates required structured fields and confidence scores from an extracted document."""
    validations: List[DocumentFieldValidation] = []

    if isinstance(extracted_document, ExtractedInvoiceFields):
        document_type = "invoice"
        required_fields = {
            "vendor_name": extracted_document.vendor_name,
            "invoice_date": extracted_document.invoice_date,
            "total_amount": extracted_document.total_amount,
        }
    elif isinstance(extracted_document, ExtractedReceiptFields):
        document_type = "receipt"
        required_fields = {
            "merchant_name": extracted_document.merchant_name,
            "transaction_date": extracted_document.transaction_date,
            "total_amount": extracted_document.total_amount,
        }
    else:
        raise ValueError("Unsupported document type for validation.")

    for field_name, value in required_fields.items():
        is_present = value is not None
        # In a real scenario, confidence would come from the Document AI entity directly.
        # For this example, we'll assign a dummy confidence.
        confidence = 1.0 if is_present else 0.0
        is_valid = is_present # Basic validation: presence implies validity for now
        validation_message = None

        if not is_present:
            validation_message = f"{field_name} is missing."

        actual_value = str(value) if value is not None else None
        expected_type = type(value).__name__ if value is not None else "str"

        validations.append(
            DocumentFieldValidation(
                field_name=field_name,
                is_present=is_present,
                confidence=confidence,
                expected_type=expected_type,
                actual_value=actual_value,
                is_valid=is_valid,
                validation_message=validation_message,
            )
        )

    # Example of validating line items presence for both types
    has_line_items = bool(extracted_document.line_items)
    validations.append(
        DocumentFieldValidation(
            field_name="line_items",
            is_present=has_line_items,
            confidence=1.0 if has_line_items else 0.0,
            expected_type="list[LineItem]",
            actual_value=str(len(extracted_document.line_items)) if has_line_items else "0",
            is_valid=has_line_items,
            validation_message="No line items found." if not has_line_items else None,
        )
    )

    return validations
