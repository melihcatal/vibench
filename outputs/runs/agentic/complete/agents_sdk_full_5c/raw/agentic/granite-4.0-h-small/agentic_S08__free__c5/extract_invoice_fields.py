import os
from document_client import StructuredDocumentClient
from document_models import InvoiceExtractionRequest, InvoiceExtractionResponse

# Using AWS Textract as the concrete provider
# The provider is identified by the client class and the AWS_ENDPOINT_URL environment variable

def extract_invoice_fields(pdf_bytes: bytes) -> InvoiceExtractionResponse:
    client = StructuredDocumentClient(service="textract")
    request = InvoiceExtractionRequest(document=pdf_bytes, document_type="invoice")
    response = client.extract(request)
    # response contains vendor, date, total, line_items etc.
    return response