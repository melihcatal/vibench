import os
import boto3

def stored_document_ocr(bucket_name, object_key):
    textract = boto3.client('textract', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = textract.detect_document_text(Document={'S3Object':{'Bucket': bucket_name, 'Name': object_key}})
    return response