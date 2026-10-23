from document_client import DocumentClient
from document_models import DocumentExtractionRequest


def invoice_summary(document_uri: str):
    client = DocumentClient()
    response = client.analyze_document(DocumentExtractionRequest(document_uri=document_uri, document_type="invoice"))
    return {
        "provider": "aws-textract",
        "summary": f"Invoice from {response.fields.get('vendor_name') or response.fields.get('vendor')}, total {response.fields.get('total') or response.fields.get('amount_due')}.",
        "fields": response.fields,
    }
