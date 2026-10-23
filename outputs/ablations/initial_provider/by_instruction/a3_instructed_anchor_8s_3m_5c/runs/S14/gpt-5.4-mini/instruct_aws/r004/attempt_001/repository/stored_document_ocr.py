import boto3

from storage_client import get_bucket_name


def run_stored_document_ocr(bucket=None, key=None, document_location=None):
    textract = boto3.client("textract")
    if document_location is None:
        document_location = {"S3Object": {"Bucket": bucket or get_bucket_name(), "Name": key}}
    return textract.analyze_document(Document={"S3Object": document_location["S3Object"]}, FeatureTypes=["TABLES", "FORMS"])
