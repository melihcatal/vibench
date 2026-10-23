import boto3

from storage_client import get_default_bucket, get_s3_client
from storage_models import normalize_key


def stored_document_ocr(bucket: str, key: str, document_api="Textract"):
    s3 = get_s3_client()
    textract = boto3.client("textract")
    s3_ref = {"S3Object": {"Bucket": bucket, "Name": normalize_key(key)}}
    if document_api == "Textract":
        return textract.detect_document_text(Document=s3_ref)
    return textract.analyze_document(Document=s3_ref, FeatureTypes=["TABLES", "FORMS"])


def stored_document_ocr_default(key: str, document_api="Textract"):
    return stored_document_ocr(get_default_bucket(), key, document_api=document_api)
