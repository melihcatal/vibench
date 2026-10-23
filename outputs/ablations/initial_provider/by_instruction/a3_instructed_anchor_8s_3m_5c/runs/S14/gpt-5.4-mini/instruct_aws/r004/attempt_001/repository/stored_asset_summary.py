import boto3


def summarize_stored_asset(text, model_id="anthropic.claude-3-haiku-20240307-v1:0", max_tokens=256):
    bedrock = boto3.client("bedrock-runtime")
    body = {"anthropic_version": "bedrock-2023-05-31", "max_tokens": max_tokens, "messages": [{"role": "user", "content": [{"type": "text", "text": text}]}]}
    return bedrock.invoke_model(modelId=model_id, body=bytes(str(body), "utf-8"))
