import boto3


def archive_summary(text: str) -> dict:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=("{\"anthropic_version\":\"bedrock-2023-05-31\",\"max_tokens\":256,\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"Summarize: " + text.replace('"', '\\"') + "\"}]}]}" ).encode(),
        contentType="application/json",
        accept="application/json",
    )
    return response
