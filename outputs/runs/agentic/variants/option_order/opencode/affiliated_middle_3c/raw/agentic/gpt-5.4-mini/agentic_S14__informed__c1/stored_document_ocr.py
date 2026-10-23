import boto3

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def run_stored_document_ocr(key: str, language_code: str = "en") -> dict:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    textract = boto3.client("textract")
    normalized_key = normalize_key(key)
    document = s3.get_object(Bucket=bucket, Key=normalized_key)
    return textract.detect_document_text(
        Document={"Bytes": document["Body"].read()},
        QueriesConfig={"Queries": []},
    )
