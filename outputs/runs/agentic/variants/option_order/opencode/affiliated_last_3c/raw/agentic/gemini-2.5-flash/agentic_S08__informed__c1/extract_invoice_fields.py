import os
from mindee import Client, product
from document_client import MindeeConfig


def extract_invoice_fields(invoice_path: str) -> dict:
    """
    Extracts vendor, date, total, and line-item fields from an invoice using Mindee.
    """
    mindee_client = Client(api_key=os.environ.get(MindeeConfig.API_KEY_ENV_VAR))
    input_source = mindee_client.doc_from_path(invoice_path)
    result = mindee_client.parse(input_source, product.InvoiceV4)

    extracted_data = {
        "vendor_name": result.document.inference.prediction.supplier_name.value,
        "invoice_date": result.document.inference.prediction.date.value,
        "total_amount": result.document.inference.prediction.total_amount.value,
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_amount,
            }
            for item in result.document.inference.prediction.line_items
        ],
    }
    return extracted_data
