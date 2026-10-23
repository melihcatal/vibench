import os
import json
import boto3
from storage_client import get_textract_client
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse

def run_ocr_on_stored_document(request: StoredDocumentOcrRequest) -> StoredDocumentOcrResponse:
    textract_client = get_textract_client()

    # AWS Textract `detect_document_text` is used for synchronous OCR from an S3 object
    # For larger files, start_document_text_detection (async) would be more appropriate.
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': request.bucket,
                'Name': request.key
            }
        }
    )

    extracted_text = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            extracted_text.append(item['Text'])
    
    full_text = "\n".join(extracted_text)

    return StoredDocumentOcrResponse(text=full_text)
