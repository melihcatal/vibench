import os
from typing import Dict, Any
from mindee import Client, documents
from document_models import InvoiceFields

mindee_client = Client(api_key=os.getenv("MINDEE_API_KEY"))


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    with open(file_path, "rb") as file:
        input_doc = mindee_client.doc_from_path(file_path)
        api_response = input_doc.parse(documents.TypeInvoiceV4)
        
    if not api_response.document:
        raise ValueError("No invoice data extracted")
    
    invoice_data = api_response.document
    
    result = {
        "vendor": invoice_data.supplier.name.value if invoice_data.supplier else None,
        "date": invoice_data.date.value.isoformat() if invoice_data.date else None,
        "total": invoice_data.total_amount.value if invoice_data.total_amount else None,
        "line_items": [
            {
                "description": item.description.value if item.description else None,
                "quantity": item.quantity.value if item.quantity else None,
                "unit_price": item.unit_price.value if item.unit_price else None,
                "total_price": item.total_amount.value if item.total_amount else None,
            }
            for item in invoice_data.line_items
        ],
        "confidence": invoice_data.confidence,
    }
    return result