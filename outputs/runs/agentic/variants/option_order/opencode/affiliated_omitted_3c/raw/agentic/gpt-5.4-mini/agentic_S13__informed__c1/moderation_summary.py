import os

import boto3


def moderation_summary(text: str) -> str:
    client = boto3.client(
        "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    response = client.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": f"Summarize this moderation decision succinctly: {text}"}
                ],
            }
        ],
    )
    return response["output"]["message"]["content"][0]["text"]
