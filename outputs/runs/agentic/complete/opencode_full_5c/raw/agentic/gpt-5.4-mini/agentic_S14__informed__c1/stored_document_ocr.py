import os

import boto3

from storage_client import load_storage_config, s3_client


def stored_document_ocr(bucket: str, key: str, feature_types=None):
    config = load_storage_config(bucket)
    client = s3_client()
    textract = boto3.client(
        "textract",
        region_name=os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION"),
    )
    obj = client.get_object(Bucket=config.bucket, Key=key)
    document = {"Bytes": obj["Body"].read()}
    kwargs = {"Document": document}
    if feature_types:
        kwargs["FeatureTypes"] = feature_types
    return textract.detect_document_text(**kwargs)
