import boto3


def moderation_summary(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    text = payload.get("text", "") if isinstance(payload, dict) else str(payload)
    response = client.converse(modelId="anthropic.claude-3-haiku-20240307-v1:0", messages=[{"role": "user", "content": [{"text": f"Summarize moderation decision: {text}"}]}])
    return {"summary": response["output"]["message"]["content"][0]["text"]}
