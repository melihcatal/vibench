import os
import json
import boto3
from botocore.exceptions import ClientError
from model_client import get_bedrock_runtime_client
from model_models import InvocationRequest, InvocationResponse

def invoke_platform_model(request: InvocationRequest) -> InvocationResponse:
    """Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client."""
    bedrock_runtime_client = get_bedrock_runtime_client()

    # Construct the body for the Anthropic Claude model
    body = json.dumps({
        "messages": [{
            "role": "user",
            "content": request.prompt
        }],
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": request.max_tokens or 1000,
        "temperature": request.temperature or 0.7
    })

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=request.model_id or "anthropic.claude-3-haiku-20240307-v1:0",
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        generated_text = "".join([block["text"] for block in response_body.get("content", []) if block["type"] == "text"])
        
        # Extract usage metadata if available
        usage = response_body.get("usage", {})
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")

        return InvocationResponse(
            generated_text=generated_text,
            model_id=request.model_id,
            input_token_count=input_tokens,
            output_token_count=output_tokens
        )
    except ClientError as e:
        raise RuntimeError(f"Bedrock model invocation failed: {e}")
