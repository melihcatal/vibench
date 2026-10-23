import boto3

from storage_client import get_s3_client, get_storage_config


bedrock_runtime = boto3.client("bedrock-runtime", region_name=get_storage_config().region_name)


def summarize_stored_asset(bucket: str, key: str) -> str:
    s3 = get_s3_client(get_storage_config())
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8", errors="ignore")
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "messages": [{"role": "user", "content": f"Summarize the following content concisely:\n\n{text}"}],
    }
    response = bedrock_runtime.converse(modelId="anthropic.claude-3-sonnet-20240229-v1:0", messages=payload["messages"], inferenceConfig={"maxTokens": 300})
    return response
