import boto3

from storage_client import get_default_bucket, get_s3_client
from storage_models import normalize_key


def stored_asset_summary(
    bucket: str, key: str, model_id: str = "amazon.titan-text-express-v1"
):
    s3 = get_s3_client()
    bedrock = boto3.client("bedrock-runtime")
    obj = s3.get_object(Bucket=bucket, Key=normalize_key(key))
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    prompt = f"Summarize the following content:\n{text}"
    return bedrock.invoke_model(
        modelId=model_id,
        body=(f'{{"inputText": {prompt!r}}}').encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )


def stored_asset_summary_default(
    key: str, model_id: str = "amazon.titan-text-express-v1"
):
    return stored_asset_summary(get_default_bucket(), key, model_id=model_id)
