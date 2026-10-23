import boto3


def get_textract_client():
    return boto3.client("textract", region_name="us-east-1")


def get_alibaba_ocr_client():
    return alibabacloud_ocr_api.Client(
        access_key_id="your-access-key-id", access_key_secret="your-access-key-secret"
    )
