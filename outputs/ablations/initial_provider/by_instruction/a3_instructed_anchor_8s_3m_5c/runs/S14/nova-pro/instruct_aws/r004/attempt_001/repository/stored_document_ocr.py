import boto3

def ocr_document(bucket, key):
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(Document={'S3Object':{'Bucket': bucket, 'Name': key}})
    return response