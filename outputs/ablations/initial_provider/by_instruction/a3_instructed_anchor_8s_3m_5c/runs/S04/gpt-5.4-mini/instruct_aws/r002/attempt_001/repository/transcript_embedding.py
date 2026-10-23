import boto3

from speech_client import load_config


def transcript_embedding(text: str) -> list[float]:
    config = load_config()
    client = boto3.client(
        "bedrock-runtime",
        region_name=config.aws_region,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{\"inputText\":\"" + text.replace('"', '\\"') + "\"}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return []
