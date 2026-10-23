import os
from typing import Dict, List, Optional
from mindee import Client, documents
from mindee.input import LocalInputSource


def extract_invoice_fields(file_path: str) -> Dict[str, Optional[str]]:
    """
    Extracts structured fields from an invoice document using Mindee Invoice OCR.
    Requires MINDEE_API_KEY environment variable.
    """
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set")

    client = Client(api_key=api_key)
    input_source = LocalInputSource(file_path)
    response = client.parse(
        document_type=documents.TypeInvoiceV4, input_source=input_source
    )

    invoice_data = response.document.inference.prediction
    return {
        "invoice_number": invoice_data.invoice_number.value
        if invoice_data.invoice_number
        else None,
        "date": invoice_data.date.value if invoice_data.date else None,
        "total_amount": invoice_data.total_amount.value
        if invoice_data.total_amount
        else None,
        "supplier_name": invoice_data.supplier_name.value
        if invoice_data.supplier_name
        else None,
        "customer_name": invoice_data.customer_name.value
        if invoice_data.customer_name
        else None,
        "tax_amount": invoice_data.taxes[0].value if invoice_data.taxes else None,
        "currency": invoice_data.locale.currency if invoice_data.locale else None,
    }


def document_field_extraction(file_path: str) -> Dict[str, Optional[str]]:
    """
    Extracts structured fields from a document using Mindee Invoice OCR.
    """
    return extract_invoice_fields(file_path)
