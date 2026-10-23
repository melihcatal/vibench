import boto3
from storage_client import get_textract_client
from storage_models import StorageConfig, OCRRequest

def stored_document_ocr(request: OCRRequest, config: StorageConfig):
    textract_client = get_textract_client(config)
    response = textract_client.detect_document_text(
        Document={'S3Object': {'Bucket': config.bucket, 'Name': request.object_name}}
    )
    detected_text = []
    for item in response.get('Blocks', []):
        if item['BlockType'] == 'LINE':
            detected_text.append(item['Text'])
    return {"detected_text": "\n".join(detected_text)}
