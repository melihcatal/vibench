import boto3

from storage_client import get_bucket_name, get_s3_client


def stored_document_ocr(bucket=None, key=None, language_code="en"):
    textract = boto3.client("textract", region_name=get_s3_client().meta.region_name)
    return textract.analyze_document(
        Document={"S3Object": {"Bucket": get_bucket_name(bucket), "Name": key}},
        FeatureTypes=["FORMS", "TABLES"],
    )
