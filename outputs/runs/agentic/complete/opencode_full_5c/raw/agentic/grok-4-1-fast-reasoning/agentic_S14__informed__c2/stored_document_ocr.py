import boto3
from storage_client import get_s3_client, get_aws_session

def stored_document_ocr(bucket: str, key: str) -&gt; str:
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    document_bytes = obj['Body'].read()
    session = get_aws_session()
    textract_client = session.client('textract')
    response = textract_client.detect_document_text(Document={'Bytes': document_bytes})
    text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + '\n'
    return text.strip()