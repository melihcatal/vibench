"""Return model output together with Amazon Bedrock platform metadata.

Invokes anthropic.claude-3-sonnet-20240229-v1:0 on Bedrock via boto3
and returns the generated text alongside usage statistics, model ID,
stop reason, and other provider-specific metadata fields.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
from typing import Any, Dict, Optional

from model_client import get_bedrock_runtime_client
from model_models import PlatformModelRequest, PlatformModelResponse, extract_text_from_bedrock_response

BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def collect_platform_metadata(
    prompt: str,
    model_id: str = BEDROCK_MODEL_ID,
    system_prompt: str = "",
    max_tokens: int = 1024,
    temperature: float = 0.7,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> PlatformModelResponse:
    """Invoke a Bedrock model and return output with full provider metadata.

    Calls the bedrock-runtime invoke_model API for
    anthropic.claude-3-sonnet-20240229-v1:0 and returns a
    PlatformModelResponse containing:
    - generated_text: the model output
    - model_id: the invoked Bedrock model identifier
    - stop_reason: why generation ended (e.g., end_turn, max_tokens)
    - input_tokens / output_tokens: token usage from Bedrock
    - raw_response: the full parsed JSON from the provider
    - usage_metadata: nested usage dict with Bedrock-specific fields
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
    model_id_returned = response.get("modelId", request.model_id)

    metadata = PlatformModelResponse(
        generated_text=generated_text,
        model_id=model_id_returned,
        stop_reason=response_body.get("stop_reason", "unknown"),
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
        raw_response=response_body,
        usage_metadata=usage,
    )
    return metadata


def format_metadata_summary(response: PlatformModelResponse) -> Dict[str, Any]:
    """Format a human-readable metadata summary dict."""
    return {
        "model_id": response.model_id,
        "stop_reason": response.stop_reason,
        "input_tokens": response.input_tokens,
        "output_tokens": response.output_tokens,
        "generated_text_length": len(response.generated_text),
        "provider": "Amazon Bedrock",
    }


if __name__ == "__main__":
    result = collect_platform_metadata(
        prompt="Summarize the key principles of microservices architecture.",
        max_tokens=256,
    )
    summary = format_metadata_summary(result)
    print(json.dumps(summary, indent=2))
    print(f"\nOutput:\n{result.generated_text}")
