import boto3

from storage_models import normalize_text


def stored_asset_summary(text, model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"):
    bedrock = boto3.client("bedrock-runtime")
    prompt = f"Summarize the following asset content:\n\n{normalize_text(text)}"
    response = bedrock.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0.2},
    )
    return response["output"]["message"]["content"][0].get("text", "")
