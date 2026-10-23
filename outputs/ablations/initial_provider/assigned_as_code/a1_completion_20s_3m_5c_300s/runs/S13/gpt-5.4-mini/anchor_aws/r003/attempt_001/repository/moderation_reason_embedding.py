import boto3


def moderation_reason_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    text = payload.get("text", "") if isinstance(payload, dict) else str(payload)
    response = client.invoke_model(modelId="amazon.titan-embed-text-v1", body=f'{{"inputText":"{text}"}}', contentType="application/json", accept="application/json")
    body = response["body"].read().decode("utf-8")
    return {"embedding": body}
