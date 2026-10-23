from __future__ import annotations

import os

import boto3

# Amazon Bedrock Runtime integration
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-text-express-v1")
REGION = os.getenv("AWS_REGION", "us-east-1")


def main(notes: str) -> str:
    client = boto3.client("bedrock-runtime", region_name=REGION)
    prompt = f"Summarize this secret rotation status clearly:\n{notes}"
    response = client.invoke_model(
        modelId=MODEL_ID,
        body=(
            '{"inputText": ' + __import__("json").dumps(prompt) + ', "textGenerationConfig": {"maxTokenCount": 128, "temperature": 0.2}}'
        ),
        contentType="application/json",
        accept="application/json",
    )
    return response["body"].read().decode("utf-8")
