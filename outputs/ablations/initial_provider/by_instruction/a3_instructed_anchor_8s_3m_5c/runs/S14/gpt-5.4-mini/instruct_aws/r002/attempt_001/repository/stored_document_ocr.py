import boto3

from storage_client import default_bucket, s3_client
from storage_models import normalize_key, response_payload


def stored_document_ocr(bucket=None, key=None, textract_feature_types=None):
    bucket_name = default_bucket(bucket)
    object_key = normalize_key(key)
    client = boto3.client("textract")
    params = {
        "Document": {"S3Object": {"Bucket": bucket_name, "Name": object_key}},
        "FeatureTypes": list(textract_feature_types or ["FORMS", "TABLES"]),
    }
    result = client.analyze_document(**params)
    return response_payload(provider="aws", service="textract", bucket=bucket_name, key=object_key, blocks=result.get("Blocks", []), model_version=result.get("AnalyzeDocumentModelVersion"))
