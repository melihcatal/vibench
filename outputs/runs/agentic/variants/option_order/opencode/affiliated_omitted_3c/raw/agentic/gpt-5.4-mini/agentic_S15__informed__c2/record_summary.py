import boto3


def summarize_record(record):
    client = boto3.client("bedrock-runtime")
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": f"Summarize this record: {record}"}],
    }
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=str(body).encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return response
