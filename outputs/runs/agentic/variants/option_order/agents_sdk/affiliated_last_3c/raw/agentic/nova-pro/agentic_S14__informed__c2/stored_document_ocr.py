import boto3

def stored_document_ocr(bucket_name, object_name):
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(Document={'S3Object':{'Bucket':bucket_name,'Name':object_name}})
    return response