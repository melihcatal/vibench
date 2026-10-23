"""Invoke a provider-managed model through an Amazon Bedrock client.

Uses boto3 to call the bedrock-runtime invoke_model API with
anthropic.claude-3-sonnet-20240229-v1:0 on Amazon Bedrock.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
from typing import Optional

from model_client import get_bedrock_runtime_client
from model_models import PlatformModelRequest, PlatformModelResponse, extract_text_from_bedrock_response

BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def invoke_platform_model(
    prompt: str,
    model_id: str = BEDROCK_MODEL_ID,
    system_prompt: str = "",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> PlatformModelResponse:
    """Invoke an Amazon Bedrock model and return a normalized response.

    Uses the boto3 bedrock-runtime client to send an InvokeModel request
    to the anthropic.claude-3-sonnet-20240229-v1:0 model on Bedrock.
    """
    request = PlatformModelRequest.from_text(
        text=prompt,
        model_id=model_id,
        system_prompt=system_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    client = get_bedrock_runtime_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    body_bytes = request.to_bedrock_payload()

    response = client.invoke_model(
        modelId=request.model_id,
        body=body_bytes,
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response["body"].read())
    generated_text = extract_text_from_bedrock_response(response_body)

    usage = response_body.get("usage", {})
    return PlatformModelResponse(
        generated_text=generated_text,
        model_id=request.model_id,
        stop_reason=response_body.get("stop_reason", "unknown"),
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
        raw_response=response_body,
        usage_metadata=usage,
    )


if __name__ == "__main__":
    result = invoke_platform_model(
        prompt="Explain the benefits of serverless architecture in three sentences.",
        max_tokens=256,
        temperature=0.5,
    )
    print(result.generated_text)
    print(f"Tokens: input={result.input_tokens}, output={result.output_tokens}")
