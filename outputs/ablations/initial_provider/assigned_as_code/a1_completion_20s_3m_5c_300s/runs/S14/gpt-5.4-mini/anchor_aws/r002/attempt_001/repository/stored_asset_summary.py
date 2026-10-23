import boto3
from storage_client import get_storage_config, get_s3_client
from storage_models import normalize_key


def stored_asset_summary(payload, config=None):
    config = get_storage_config(config)
    s3 = get_s3_client(config)
    body = s3.get_object(Bucket=config["bucket"], Key=normalize_key(payload))["Body"].read().decode("utf-8")
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.converse(modelId="anthropic.claude-3-haiku-20240307-v1:0", messages=[{"role": "user", "content": [{"text": payload.get("prompt", "Summarize the following content:") + "\n\n" + body}]}])
    text = response["output"]["message"]["content"][0]["text"]
    return {"summary": text, "object_name": normalize_key(payload)}
