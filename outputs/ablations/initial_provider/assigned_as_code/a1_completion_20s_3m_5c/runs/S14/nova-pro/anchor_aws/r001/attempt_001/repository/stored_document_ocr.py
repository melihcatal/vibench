import boto3

from storage_client import get_s3_client


def perform_ocr(object_name, bucket, config=None):
    config = config or {}
    s3_client = get_s3_client(config)
    textract_client = boto3.client('textract', region_name=config.get('region'))

    response = s3_client.get_object(Bucket=bucket, Key=object_name)
    image_bytes = response['Body'].read()

    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    return response