import boto3

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def summarize_stored_asset(key: str) -> dict:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    bedrock = boto3.client("bedrock-runtime")
    text = (
        s3.get_object(Bucket=bucket, Key=normalize_key(key))["Body"]
        .read()
        .decode("utf-8", errors="ignore")
    )
    return bedrock.converse(
        modelId="amazon.nova-lite-v1:0",
        messages=[
            {"role": "user", "content": [{"text": f"Summarize this asset:\n{text}"}]}
        ],
    )
