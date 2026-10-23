from document_client import DocumentClient
from document_models import DocumentTextractRequest, DocumentTextractResponse
import logging

logger = logging.getLogger(__name__)

def extract_text(request: DocumentTextractRequest) -> DocumentTextractResponse:
    client = DocumentClient()
    textract_client = client.textract_client

    if request.document_content_bytes:
        response = textract_client.detect_document_text(Document={'Bytes': request.document_content_bytes})
    elif request.s3_bucket and request.s3_key:
        response = textract_client.detect_document_text(Document={'S3Object': {'Bucket': request.s3_bucket, 'Name': request.s3_key}})
    else:
        raise ValueError("Either document_content_bytes or s3_bucket/s3_key must be provided.")

    extracted_text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text.append(item['Text'])

    return DocumentTextractResponse(text="\n".join(extracted_text), raw_response=response)
