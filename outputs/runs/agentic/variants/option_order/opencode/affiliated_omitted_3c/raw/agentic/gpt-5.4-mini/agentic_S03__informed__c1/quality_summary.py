import boto3


def quality_summary(text: str) -> str:
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=("Summarize translation quality issues: " + text).encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return response["body"].read().decode("utf-8")
