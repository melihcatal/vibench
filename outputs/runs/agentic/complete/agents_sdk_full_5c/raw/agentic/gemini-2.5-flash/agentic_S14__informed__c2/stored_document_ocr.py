import boto3
from typing import Dict, Any
from storage_client import get_textract_client, get_s3_bucket_name
from storage_models import OCRRequest

def run_ocr_on_stored_document(request: OCRRequest) -> Dict[str, Any]:
    textract_client = get_textract_client()

    try:
        response = textract_client.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': request.bucket_name,
                    'Name': request.object_key,
                }
            }
        )
        return response
    except textract_client.exceptions.ClientError as e:
        raise RuntimeError(f"Amazon Textract failed to process document: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during OCR: {e}")
