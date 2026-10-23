import boto3
from storage_client import get_aws_creds
from storage_models import download_object_as_bytes

def stored_document_ocr(bucket: str, key: str) -> str:
    s3 = boto3.client('s3', **get_aws_creds())
    document_bytes = download_object_as_bytes(s3, bucket, key)
    textract = boto3.client('textract', **get_aws_creds())
    resp = textract.detect_document_text(Document={'Bytes': document_bytes})
    text = ''
    for block in resp['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + '\n'
    return text.strip()