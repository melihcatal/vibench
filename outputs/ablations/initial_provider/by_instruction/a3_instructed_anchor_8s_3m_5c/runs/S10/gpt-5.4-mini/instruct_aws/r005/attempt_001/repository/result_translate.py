import json
import os

import boto3


def result_translate(text: str, target_language: str) -> str:
    client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    response = client.invoke_model(
        modelId=os.environ.get("AWS_BEDROCK_TRANSLATION_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0"),
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "temperature": 0.2,
                "messages": [{"role": "user", "content": [{"type": "text", "text": f"Translate the following text to {target_language}.\n\n{text}"}]}],
            }
        ),
    )
    body = json.loads(response["body"].read())
    return body["content"][0]["text"]
