import os

import boto3


def summarize_meeting(transcript: str) -> str:
    client = boto3.client("bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    body = '{"inputText":"Summarize this meeting transcript:\n' + transcript.replace('"', '\\"') + '","textGenerationConfig":{"maxTokenCount":256,"temperature":0.2}}'
    response = client.invoke_model(body=body, modelId="anthropic.claude-3-haiku-20240307-v1:0", accept="application/json", contentType="application/json")
    return response["body"].read().decode("utf-8")
