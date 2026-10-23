import boto3
from botocore.exceptions import ClientError


def run_ocr_on_stored_document(object_name):
    textract_client = boto3.client('textract', region_name='your-region')
    try:
        response = textract_client.detect_document_text(
            Document={'S3Object':{'Bucket':'your-bucket-name','Name':object_name}}
        )
    except ClientError as e:
        raise e
    return response