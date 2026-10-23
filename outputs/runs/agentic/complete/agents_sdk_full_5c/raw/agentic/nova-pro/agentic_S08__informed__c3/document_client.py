import os

def get_textract_client():
    return boto3.client('textract', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def get_alibaba_ocr_client():
    from alibabacloud_ocr_api import Client as OcrClient
    return OcrClient(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'), os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))