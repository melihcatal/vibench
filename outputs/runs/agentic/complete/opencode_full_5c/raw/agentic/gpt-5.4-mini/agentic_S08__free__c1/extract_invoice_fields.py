from document_client import StructuredDocumentClient
from document_models import DocumentRequest


def extract_invoice_fields(document_text: str):
    client = StructuredDocumentClient()
    return client.extract(
        DocumentRequest(document_text=document_text, document_type="invoice"),
        {
            "vendor": "string",
            "date": "string",
            "total": "number",
            "line_items": [
                {"description": "string", "quantity": "number", "amount": "number"}
            ],
        },
    )
