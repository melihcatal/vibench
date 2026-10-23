import boto3
from botocore.exceptions import ClientError
from storage_client import create_aws_client


def ocr_document(bucket: str, key: str, region: str = "us-east-1") -> str:
    textract = create_aws_client("textract", region)
    try:
        resp = textract.detect_document_text(
            Document={"S3Object": {"Bucket": bucket, "Name": key}}
        )
        text = ""
        for block in resp["Blocks"]:
            if block["BlockType"] == "LINE":
                text += block["Text"] + "\n"
        return text.strip()
    except ClientError as e:
        raise RuntimeError(f"OCR failed: {str(e)}")
