import json
import os
from model_client import get_bedrock_runtime_client
from model_models import get_claude_request_body, parse_claude_response

def get_claude_generation_and_metadata(prompt: str, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> dict:
    bedrock_runtime = get_bedrock_runtime_client()
    body = get_claude_request_body(prompt)

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=body
    )

    response_body_str = response["body"].read().decode("utf-8")
    generated_text = parse_claude_response(response_body_str)

    claude_response_json = json.loads(response_body_str)
    
    usage_metadata = claude_response_json.get("usage", {})
    
    platform_metadata = {
        "model_id": model_id,
        "input_tokens": usage_metadata.get("input_tokens"),
        "output_tokens": usage_metadata.get("output_tokens"),
        "stop_reason": claude_response_json.get("stop_reason"),
        "stop_sequence": claude_response_json.get("stop_sequence"),
        "invocation_response_content_type": response.get("contentType")
    }

    return {
        "generated_text": generated_text,
        "platform_metadata": platform_metadata
    }
