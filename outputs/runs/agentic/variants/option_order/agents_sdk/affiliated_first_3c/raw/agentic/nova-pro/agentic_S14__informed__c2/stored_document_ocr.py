import boto3

textract = boto3.client('textract')

def stored_document_ocr(bucket_name, object_name):
    response = textract.detect_document_text(Document={'S3Object':{'Bucket': bucket_name,'Name': object_name}})
    return response