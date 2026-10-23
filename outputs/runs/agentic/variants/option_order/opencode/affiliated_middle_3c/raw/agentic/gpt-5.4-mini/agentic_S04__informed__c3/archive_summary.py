import boto3


def archive_summary(transcript_text: str):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    return client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=(
            "{"
            + f'"prompt":"Summarize this transcript briefly: {transcript_text}"'
            + "}"
        ).encode(),
        contentType="application/json",
        accept="application/json",
    )
