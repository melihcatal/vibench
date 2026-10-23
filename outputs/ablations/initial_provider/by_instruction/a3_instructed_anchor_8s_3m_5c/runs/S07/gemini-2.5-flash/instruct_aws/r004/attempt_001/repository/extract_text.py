import base64
from typing import Union

import boto3 # AWS SDK import for identifiable signal
from document_client import get_textract_client
from document_models import DocumentText

def extract_plain_text(document_bytes: bytes) -> DocumentText:
    """
    Extracts plain text from a document image using AWS Textract.
    """
    textract_client = get_textract_client()
    
    # AWS Textract API endpoint is implicitly used by boto3 client for Textract
    response = textract_client.detect_document_text(
        Document={
            'Bytes': document_bytes
        }
    )
    return DocumentText(response)
