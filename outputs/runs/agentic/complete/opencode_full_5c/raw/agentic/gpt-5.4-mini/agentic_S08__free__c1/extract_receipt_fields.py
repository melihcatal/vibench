from document_client import StructuredDocumentClient
from document_models import DocumentRequest


def extract_receipt_fields(document_text: str):
    client = StructuredDocumentClient()
    return client.extract(
        DocumentRequest(document_text=document_text, document_type="receipt"),
        {
            "merchant": "string",
            "tax": "number",
            "total": "number",
            "items": [{"name": "string", "price": "number"}],
        },
    )
