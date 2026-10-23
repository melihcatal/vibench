import os
from storage_client import ManagedStorageClient
from typing import Tuple

# Concrete OCR provider: AWS Textract (managed service)
import boto3
from botocore.exceptions import ClientError

def ocr_from_stored_document(bucket: str, key: str) -> Tuple[str, str]:
    """Extract text from a PDF/image stored in object storage using AWS Textract.\n\n    Returns (plain_text, blocks_json). The Textract response is parsed for readability.\n    """
    textract = boto3.client('textract')
    # Download the object first (could stream, but simplicity)
    obj = ManagedStorageClient().get_object(Bucket=bucket, Key=key)
    document = {'Bytes': obj['Body'].read()}

    try:
        response = textract.detect_document_text(Document=document)
    except ClientError as e:
        raise RuntimeError(f"Textract error: {e}")

    plain_text = \"\n\".join(item['Text'] for item in response.get('Blocks', []) if item['BlockType'] == 'LINE')
    blocks_json = response  # raw JSON if downstream processing needs it
    return plain_text, blocks_json
