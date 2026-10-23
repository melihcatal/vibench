import os
from document_client import StructuredDocumentClient
from document_models import ReceiptExtractionRequest, ReceiptExtractionResponse

# Using AWS Textract as the concrete provider
# The provider is identified by the client class and the AWS_ENDPOINT_URL environment variable

def extract_receipt_fields(pdf_bytes: bytes) -> ReceiptExtractionResponse:
    client = StructuredDocumentClient(service="textract")
    request = ReceiptExtractionRequest(document=pdf_bytes, document_type="receipt")
    response = client.extract(request)
    # response contains merchant, tax, total, items etc.
    return response