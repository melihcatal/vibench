import boto3


def collect_platform_metadata(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.converse(
        modelId="us.amazon.nova-pro-v1:0",
        messages=[{"role": "user", "content": [{"text": payload["text"]}]}],
    )
    metadata = {
        "usage": response["usage"],
        "resourceId": response["responseMetadata"]["requestId"],
        "modelHandle": response["modelId"],
    }
    return metadata