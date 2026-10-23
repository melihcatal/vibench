from typing import Union
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense


def normalize_expense(
    extracted_document: Union[ExtractedInvoice, ExtractedReceipt], document_type: str
) -> NormalizedExpense:
    if document_type == "invoice":
        if not isinstance(extracted_document, ExtractedInvoice):
            raise ValueError("Expected ExtractedInvoice for invoice document type.")

        line_items = []
        if extracted_document.line_items:
            for item in extracted_document.line_items:
                line_items.append(
                    {
                        "description": item.description,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                        "total_price": item.total_price,
                    }
                )

        return NormalizedExpense(
            document_type="invoice",
            vendor_name=extracted_document.vendor_name,
            transaction_date=extracted_document.invoice_date,
            total_amount=extracted_document.invoice_total,
            line_items=line_items,
            original_data=extracted_document.dict(),
        )
    elif document_type == "receipt":
        if not isinstance(extracted_document, ExtractedReceipt):
            raise ValueError("Expected ExtractedReceipt for receipt document type.")

        line_items = []
        if extracted_document.items:
            for item in extracted_document.items:
                line_items.append(
                    {
                        "description": item.description,
                        "quantity": item.quantity,
                        "price": item.price,
                    }
                )

        return NormalizedExpense(
            document_type="receipt",
            vendor_name=extracted_document.merchant_name,
            transaction_date=None,  # Receipts often don't have a specific 'invoice date' equivalent that's easily extracted by generic models
            total_amount=extracted_document.total_amount,
            line_items=line_items,
            original_data=extracted_document.dict(),
        )
    else:
        raise ValueError("Unsupported document type. Must be 'invoice' or 'receipt'.")
