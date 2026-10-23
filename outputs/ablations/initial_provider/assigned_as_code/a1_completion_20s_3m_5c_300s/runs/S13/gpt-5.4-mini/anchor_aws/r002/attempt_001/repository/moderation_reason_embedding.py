import boto3


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.invoke_model(body=f'{{"inputText":"{payload["reason"]}"}}', modelId=config.get("model_id", "amazon.titan-embed-text-v1"), accept="application/json", contentType="application/json")
    return {"embedding": response["body"].read()}
