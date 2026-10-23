import boto3

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_object_key, normalize_text


def stored_document_ocr(key: str, bucket: str = None, document_format: str = "PDF"):
    textract = boto3.client("textract")
    s3 = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    object_key = normalize_object_key(key)
    s3.head_object(Bucket=bucket_name, Key=object_key)
    response = textract.detect_document_text(Document={"S3Object": {"Bucket": bucket_name, "Name": object_key}}, DocumentReadMode=document_format)
    return [normalize_text(block.get("Text")) for block in response.get("Blocks", []) if block.get("BlockType") == "LINE"]
