import boto3

from storage_client import get_default_bucket, get_s3_client
from storage_models import normalize_key


def asset_metadata_embedding(
    bucket: str, key: str, model_id: str = "amazon.titan-embed-text-v1"
):
    s3 = get_s3_client()
    bedrock = boto3.client("bedrock-runtime")
    meta = s3.head_object(Bucket=bucket, Key=normalize_key(key))
    obj = s3.get_object(Bucket=bucket, Key=normalize_key(key))
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    payload = {
        "inputText": f"{meta.get('ContentType', '')} {meta.get('ContentLength', '')} {text}"
    }
    return bedrock.invoke_model(
        modelId=model_id,
        body=str(payload).replace("'", '"').encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )


def asset_metadata_embedding_default(
    key: str, model_id: str = "amazon.titan-embed-text-v1"
):
    return asset_metadata_embedding(get_default_bucket(), key, model_id=model_id)
