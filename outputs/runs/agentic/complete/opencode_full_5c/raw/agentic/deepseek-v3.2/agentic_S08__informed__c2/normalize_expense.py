import json
from typing import Dict, Any, List, Union
from document_models import InvoiceData, ReceiptData, ExpenseRecord, DocumentNormalizer


def normalize_expense(
    extracted_data: Union[InvoiceData, ReceiptData], document_type: str = None
) -> Dict[str, Any]:
    """
    Normalize extracted expense fields into a standard JSON schema.

    Args:
        extracted_data: InvoiceData or ReceiptData object
        document_type: Optional document type override

    Returns:
        Normalized expense record in standard JSON schema
    """
    if document_type is None:
        if isinstance(extracted_data, InvoiceData):
            document_type = "invoice"
        elif isinstance(extracted_data, ReceiptData):
            document_type = "receipt"
        else:
            document_type = "unknown"

    if isinstance(extracted_data, InvoiceData):
        expense_record = DocumentNormalizer.create_expense_record(
            extracted_data, document_type
        )
    elif isinstance(extracted_data, ReceiptData):
        expense_record = ExpenseRecord(
            document_type=document_type,
            vendor=extracted_data.merchant_name,
            date=extracted_data.transaction_date,
            total=extracted_data.total_amount,
            currency="USD",
            line_items=extracted_data.items,
            metadata={
                "tax_amount": extracted_data.tax_amount,
                "item_count": len(extracted_data.items),
            },
            confidence=extracted_data.confidence_score,
        )
    else:
        raise ValueError(f"Unsupported data type: {type(extracted_data)}")

    return expense_record_to_dict(expense_record)


def expense_record_to_dict(expense_record: ExpenseRecord) -> Dict[str, Any]:
    """
    Convert ExpenseRecord to dictionary.

    Args:
        expense_record: ExpenseRecord object

    Returns:
        Dictionary representation
    """
    return {
        "document_type": expense_record.document_type,
        "vendor": expense_record.vendor,
        "date": expense_record.date,
        "total": expense_record.total,
        "currency": expense_record.currency,
        "line_items": expense_record.line_items,
        "metadata": expense_record.metadata,
        "extracted_at": expense_record.extracted_at,
        "confidence": expense_record.confidence,
    }


def normalize_to_json_schema(
    extracted_data: Union[InvoiceData, ReceiptData], document_type: str = None
) -> str:
    """
    Normalize extracted data to JSON schema string.

    Args:
        extracted_data: InvoiceData or ReceiptData object
        document_type: Optional document type override

    Returns:
        JSON string of normalized expense record
    """
    normalized_dict = normalize_expense(extracted_data, document_type)
    return json.dumps(normalized_dict, indent=2, default=str)


def validate_normalized_schema(normalized_data: Dict[str, Any]) -> bool:
    """
    Validate that normalized data conforms to expected schema.

    Args:
        normalized_data: Normalized expense record dictionary

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["document_type", "vendor", "date", "total", "currency"]

    for field in required_fields:
        if field not in normalized_data:
            return False

    if not isinstance(normalized_data["total"], (int, float)):
        return False

    if not isinstance(normalized_data["line_items"], list):
        return False

    return True
