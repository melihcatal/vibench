import os
from storage_client import get_textract_client

def run_ocr_on_s3_document(bucket_name: str, object_key: str) -> str:
    textract_client = get_textract_client()
    
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key
            }
        }
    )

    extracted_text_blocks = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE' and 'Text' in item:
            extracted_text_blocks.append(item['Text'])
    
    return '\n'.join(extracted_text_blocks)
