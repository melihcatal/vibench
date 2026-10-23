from typing import Dict, Any, Union
from pydantic import BaseModel
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse


class NormalizedExpense(BaseModel):
    source_type: str
    vendor: str
    date: str
    total_amount: float
    tax_amount: float
    items: list[Dict[str, Union[str, float]]]


def normalize_expense(
    extracted_data: Union[InvoiceExtractionResponse, ReceiptExtractionResponse]
) -> NormalizedExpense:
    if isinstance(extracted_data, InvoiceExtractionResponse):
        return NormalizedExpense(
            source_type="invoice",
            vendor=extracted_data.vendor,
            date=extracted_data.date,
            total_amount=float(extracted_data.total),
            tax_amount=0.0,  # Placeholder for tax calculation
            items=[
                {"description": item.description, "amount": float(item.amount)}
                for item in extracted_data.line_items
            ],
        )
    elif isinstance(extracted_data, ReceiptExtractionResponse):
        return NormalizedExpense(
            source_type="receipt",
            vendor=extracted_data.merchant,
            date="",  # Receipts may not have a date in extraction
            total_amount=float(extracted_data.total),
            tax_amount=float(extracted_data.tax) if extracted_data.tax else 0.0,
            items=[
                {"description": item.description, "amount": float(item.amount)}
                for item in extracted_data.items
            ],
        )
    else:
        raise ValueError("Unsupported extraction type")