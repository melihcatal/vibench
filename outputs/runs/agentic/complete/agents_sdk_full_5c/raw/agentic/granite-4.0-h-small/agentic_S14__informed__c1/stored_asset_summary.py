import boto3
from typing import List, Dict

from .storage_client import get_s3_client
from .storage_models import StorageObject

s3 = get_s3_client()

def stored_asset_summary(bucket: str, key: str, max_pages: int = 5) -> Dict[str, str]:
    """Summarize a stored document using Amazon Textract + a quick LLM summarizer (placeholder)."""
    # First extract text (reuse OCR helper logic)
    try:
        start_response = s3.s3.start_document_text_detection(DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}})
        job_id = start_response['JobId']
        # Simple polling (real implementation should handle retries and timeouts)
        while True:
            job_status = s3.s3.get_document_text_detection(JobId=job_id)['JobStatus']
            if job_status == 'SUCCEEDED':
                blocks = s3.s3.get_document_text_detection(JobId=job_id)['Blocks']
                full_text = ' '.join([b['Text'] for b in blocks if b['BlockType'] == 'LINE'])
                break
            elif job_status == 'FAILED':
                raise RuntimeError('Textract job failed')
    except Exception as e:
        raise RuntimeError(f'Extraction failed: {e}')

    # Placeholder summarization using a local LLM (e.g., OpenAI) - omitted for brevity
    # In production you would call an LLM endpoint here
    summary = f"Summarized content of {key} (max {max_pages} pages)"[:200]
    return {'bucket': bucket, 'object': key, 'summary': summary}
