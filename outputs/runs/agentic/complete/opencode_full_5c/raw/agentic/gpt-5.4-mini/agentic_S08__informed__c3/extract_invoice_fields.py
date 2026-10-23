import os
import boto3
from document_client import build_textract_client, to_document_bytes, parse_textract_expense, require_text
from document_models import DocumentRequest, DocumentResponse

def extract_invoice_fields(request):
    payload = DocumentRequest.from_input(request)
    client = build_textract_client()
    response = client.analyze_expense(Document={'Bytes': to_document_bytes(payload.content, payload.content_type)})
    data = parse_textract_expense(response)
    return DocumentResponse(provider='amazon-textract-analyzeexpense', document_type='invoice', fields=data).to_dict()
