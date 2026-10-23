import boto3

from speech_client import load_config


def archive_summary(text: str) -> str:
    config = load_config()
    client = boto3.client(
        "bedrock-runtime",
        region_name=config.aws_region,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=("{\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"Summarize: " + text.replace('"', '\\"') + "\"}]}],\"max_tokens\":256}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return response["body"].read().decode("utf-8")
