import json
import os
from model_client import get_bedrock_runtime_client
from model_models import get_claude_request_body, parse_claude_response

def invoke_claude_model(prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> str:
    bedrock_runtime = get_bedrock_runtime_client()
    body = get_claude_request_body(prompt)

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    response_body = response["body"].read().decode("utf-8")
    return parse_claude_response(response_body)
