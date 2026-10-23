import boto3
import io
from typing import Optional

from .storage_client import get_s3_client
from .storage_models import OcrResult, StorageObject

s3 = get_s3_client()

def stored_document_ocr(bucket: str, key: str) -> Optional[OcrResult]:
    """Run Amazon Textract on a stored PDF/IMAGE and return extracted text plus layout regions."""
    try:
        # Textract requires the S3 bucket and key; output is returned as blocks
        response = s3.s3.start_document_text_detection(
            DocumentLocation={
                'S3Object': {'Bucket': bucket, 'Name': key}
            }
        )
        # Poll until job is complete – simple polling loop (real apps should handle timeouts)
        job_id = response['JobId']
        while True:
            status = s3.s3.get_document_text_detection(JobId=job_id)
            if status['JobStatus'] in ['SUCCEEDED']:
                blocks = status['Blocks']
                text_parts = []
                regions = []
                for blk in blocks:
                    if blk['BlockType'] == 'LINE':
                        text_parts.append(blk['Text'])
                    elif blk['BlockType'] == 'WORD':
                        regions.append({
                            'BoundingBox': blk.get('Geometry', {}).get('BoundingBox'),
                            'Confidence': blk.get('Confidence')
                        })
                full_text = ' '.join(text_parts)
                return OcrResult(full_text, regions)
            elif status['JobStatus'] == 'FAILED':
                raise RuntimeError(f'Textract job failed: {status.get("StatusMessage")}')
            # continue polling
    except Exception as e:
        raise RuntimeError(f'Error during OCR: {e}')
