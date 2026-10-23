import os
from document_client import DocumentClient
from document_models import DocumentExtractionRequest, DocumentExtractionResponse, ExtractedDocumentFields, LineItem

def extract_receipt_fields(document_bytes: bytes, config: dict = None) -> DocumentExtractionResponse:
    config = config or {}
    client = DocumentClient(region_name=config.get("aws_region"))
    request = DocumentExtractionRequest(document_bytes=document_bytes)
    response = client.analyze_expense(request)

    receipts = []
    for doc in response.invoices: # Textract returns a unified ExpenseDocuments, treat them as receipts here
        receipts.append(ExtractedDocumentFields(
            merchant=doc.merchant,
            tax=doc.tax,
            total=doc.total,
            items=doc.line_items # Using line_items for receipt items
        ))
    return DocumentExtractionResponse(receipts=receipts)
