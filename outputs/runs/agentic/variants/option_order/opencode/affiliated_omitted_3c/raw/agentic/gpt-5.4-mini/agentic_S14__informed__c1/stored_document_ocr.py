import boto3

from storage_client import get_s3_client, resolve_bucket


def stored_document_ocr(bucket, key, feature_types=None):
    storage = get_s3_client()
    textract = boto3.client("textract")
    obj = storage.get_object(Bucket=resolve_bucket(bucket), Key=key)
    kwargs = {"Document": {"Bytes": obj["Body"].read()}}
    if feature_types:
        kwargs["FeatureTypes"] = feature_types
    return textract.detect_document_text(**kwargs)
