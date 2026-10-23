import json
import os
from model_client import get_bedrock_runtime_client
from model_models import get_claude_request_body

def stream_claude_generation(prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
    bedrock_runtime = get_bedrock_runtime_client()
    body = get_claude_request_body(prompt)

    response = bedrock_runtime.invoke_model_with_response_stream(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    stream = response.get("body")
    if stream:
        for event in stream:
            yield event
