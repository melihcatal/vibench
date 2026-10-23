import json
import os

import boto3


def spoken_brief(text: str) -> str:
    client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    response = client.invoke_model(
        modelId=os.environ.get("AWS_BEDROCK_SPEECH_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 256,
                "temperature": 0.2,
                "messages": [{"role": "user", "content": [{"type": "text", "text": f"Rewrite the following as a short spoken brief.\n\n{text}"}]}],
            }
        ),
    )
    body = json.loads(response["body"].read())
    return body["content"][0]["text"]
