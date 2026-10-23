import boto3

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def embed_asset_metadata_and_text(key: str) -> dict:
    bucket = get_bucket_name()
    s3 = get_s3_client()
    bedrock = boto3.client("bedrock-runtime")
    metadata = s3.head_object(Bucket=bucket, Key=normalize_key(key))
    text = (
        s3.get_object(Bucket=bucket, Key=normalize_key(key))["Body"]
        .read()
        .decode("utf-8", errors="ignore")
    )
    payload = f"Metadata: {metadata.get('ContentType', '')}\nText: {text}"
    return bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=f'{{"inputText": {payload!r}}}',
        accept="application/json",
        contentType="application/json",
    )
