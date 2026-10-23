import os
import dashscope
from storage_client import get_s3_client
from storage_models import normalize_head_params

def ocr_stored_document(bucket, key):
    """Runs Amazon Textract OCR on a document stored in S3.
    Downloads the file temporarily, sends it to Textract, and returns the extracted text.
    """
    # Get S3 client
    s3 = get_s3_client()
    # Download object to a temporary file
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        s3.download_file(bucket, key, tmp_file.name)
        print(f'Downloaded {key} to temporary file for OCR.')
        # Call Textract
        response = textract_call(tmp_file.name)
        # Clean up temporary file
        os.unlink(tmp_file.name)
    # Extract plain text from the Textract response
    plain_text = flatten_textract(response)
    print('OCR completed, extracted text length:', len(plain_text))
    return plain_text

def textract_call(file_path):
    client = boto3.client('textract')
    with open(file_path, 'rb') as document:
        response = client.start_document_text_detection(Document={'Bytes': document.read()})
        job_id = response['JobId']
    # Poll job status (simplified)
    while True:
        status = client.get_document_text_detection(JobId=job_id)
        if status['JobStatus'] == 'SUCCEEDED':
            return status['Blocks']
        elif status['JobStatus'] == 'FAILED':
            raise RuntimeError('Textract job failed')
        else:
            import time
            time.sleep(2)

def flatten_textract(blocks):
    """Concatenates text from Textract Blocks into a single string.
    """
    text_parts = []
    for block in blocks:
        if block['BlockType'] == 'LINE':
            text_parts.append(block['Text'])
    return ' '.join(text_parts)
