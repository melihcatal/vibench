from typing import Dict, Any
from document_models import NormalizedExpense


def normalize_expense(
    extracted_data: Dict[str, Any], expense_type: str
) -> Dict[str, Any]:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    """
    if expense_type == "invoice":
        normalized = NormalizedExpense(
            expense_type="invoice",
            vendor_merchant_name=extracted_data.get("vendor_name", ""),
            date=extracted_data.get("invoice_date", ""),
            total_amount=extracted_data.get("total_amount", 0.0),
            tax_amount=extracted_data.get("tax_amount"),
            line_items=extracted_data.get("line_items", []),
            confidence=extracted_data.get("confidence", 0.0),
        )
    elif expense_type == "receipt":
        normalized = NormalizedExpense(
            expense_type="receipt",
            vendor_merchant_name=extracted_data.get("merchant_name", ""),
            date=extracted_data.get("transaction_date", ""),
            total_amount=extracted_data.get("total_amount", 0.0),
            tax_amount=extracted_data.get("tax_amount"),
            line_items=extracted_data.get("items", []),
            confidence=extracted_data.get("confidence", 0.0),
        )
    else:
        raise ValueError(f"Unsupported expense type: {expense_type}")

    return normalized.model_dump(exclude_none=True)
