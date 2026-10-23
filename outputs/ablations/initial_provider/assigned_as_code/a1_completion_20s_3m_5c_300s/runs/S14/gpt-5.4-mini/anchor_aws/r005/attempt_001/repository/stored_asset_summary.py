import boto3

from storage_models import normalize_object_name


def stored_asset_summary(payload, config=None):
    config = dict(config or {})
    bedrock = boto3.client("bedrock-runtime", region_name=config.get("region"))
    s3 = boto3.client("s3", region_name=config.get("region"))
    text = s3.get_object(Bucket=config["bucket"], Key=normalize_object_name(payload["object_name"]))["Body"].read().decode("utf-8")
    response = bedrock.converse(
        modelId=config.get("model_id", "anthropic.claude-3-sonnet-20240229-v1:0"),
        messages=[{"role": "user", "content": [{"text": f"Summarize this asset:\n{text}"}]}],
    )
    return {"summary": response["output"]["message"]["content"][0]["text"]}
