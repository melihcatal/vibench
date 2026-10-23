import boto3

from speech_client import get_aws_region, get_bedrock_client


def archive_summary(transcript_text: str):
    client = get_bedrock_client()
    return client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=("{\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"Summarize: " + transcript_text.replace('"', '\\"') + "\"}]}],\"max_tokens\":200}"),
        contentType="application/json",
        accept="application/json",
    )
