import json
import os

import boto3


def prompt_safety(text: str) -> bool:
    client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    response = client.invoke_model(
        modelId=os.environ.get("AWS_BEDROCK_MODERATION_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 32,
                "temperature": 0,
                "messages": [{"role": "user", "content": [{"type": "text", "text": f"Assess whether the following content is unsafe. Reply safe or unsafe only.\n\n{text}"}]}],
            }
        ),
    )
    body = json.loads(response["body"].read())
    output = body["content"][0]["text"].strip().lower()
    return output.startswith("safe")
