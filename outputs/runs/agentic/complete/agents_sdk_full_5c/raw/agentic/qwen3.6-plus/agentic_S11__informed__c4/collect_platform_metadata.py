"""Return model output together with provider platform metadata such as usage, resource IDs, or model handles.

Invokes an Amazon Bedrock model and collects comprehensive platform metadata
including token usage, model identifiers, request IDs, invocation timestamps,
and pricing-relevant information from the provider response.

Provider: Amazon Bedrock
SDK: boto3 (bedrock-runtime client)
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""

import json
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from model_client import create_bedrock_runtime_client, resolve_bedrock_credentials
from model_models import (
    PlatformModelRequest,
    PlatformModelResponse,
    parse_bedrock_response,
    normalize_prompt_for_bedrock,
)


BEDROCK_MODEL_PRICING = {
    "anthropic.claude-3-5-sonnet-20241022-v2:0": {"input": 3.00, "output": 15.00},
    "anthropic.claude-3-sonnet-20240229-v1:0": {"input": 3.00, "output": 15.00},
    "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.25, "output": 1.25},
    "meta.llama3-70b-instruct-v1:0": {"input": 2.65, "output": 3.50},
    "amazon.titan-text-express-v1": {"input": 0.80, "output": 1.60},
}


def invoke_and_collect_metadata(
    prompt: str,
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
    system_prompt: Optional[str] = None,
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> Dict[str, Any]:
    """Invoke Bedrock model and return output with comprehensive metadata.

    Args:
        prompt: User prompt.
        model_id: Bedrock model identifier.
        system_prompt: Optional system prompt.
        max_tokens: Maximum tokens to generate.
        temperature: Sampling temperature.

    Returns:
        Dict containing:
            - output: Generated text
            - model_id: Model identifier used
            - usage: Token usage counts
            - timing: Invocation timing information
            - pricing: Estimated cost
            - request_metadata: AWS request metadata
            - platform_info: Provider platform information
    """
    normalized_prompt = normalize_prompt_for_bedrock(prompt)

    request = PlatformModelRequest(
        prompt=normalized_prompt,
        system_prompt=system_prompt,
        model_id=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    credentials = resolve_bedrock_credentials()
    client = create_bedrock_runtime_client(credentials)

    payload = request.to_bedrock_payload()

    start_time = time.monotonic()
    invocation_start = datetime.now(timezone.utc).isoformat()

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload),
    )

    end_time = time.monotonic()
    invocation_end = datetime.now(timezone.utc).isoformat()

    response_body = json.loads(response["body"].read())
    result = parse_bedrock_response(response_body, model_id)

    response_metadata = response.get("ResponseMetadata", {})
    http_headers = response_metadata.get("HTTPHeaders", {})

    usage = response_body.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)

    pricing = BEDROCK_MODEL_PRICING.get(model_id, {"input": 0, "output": 0})
    estimated_cost = (
        (input_tokens / 1_000_000) * pricing["input"]
        + (output_tokens / 1_000_000) * pricing["output"]
    )

    metadata_result = {
        "output": result.text,
        "model_id": result.model_id,
        "stop_reason": result.stop_reason,
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
        },
        "timing": {
            "invocation_start": invocation_start,
            "invocation_end": invocation_end,
            "duration_ms": round((end_time - start_time) * 1000, 2),
        },
        "pricing": {
            "model": model_id,
            "input_rate_per_million": pricing["input"],
            "output_rate_per_million": pricing["output"],
            "estimated_cost_usd": round(estimated_cost, 6),
            "currency": "USD",
        },
        "request_metadata": {
            "request_id": response_metadata.get("RequestId", ""),
            "http_status": response_metadata.get("HTTPStatusCode"),
            "retry_attempts": response_metadata.get("RetryAttempts", 0),
            "x_amzn_requestid": http_headers.get("x-amzn-requestid", ""),
            "x_amzn_invocation_id": http_headers.get("x-amzn-invocation-id", ""),
        },
        "platform_info": {
            "provider": "Amazon Bedrock",
            "service": "bedrock-runtime",
            "region": credentials.get("region_name", "us-east-1"),
            "model_handle": model_id,
            "api_version": "2023-09-30",
        },
    }

    return metadata_result


def extract_usage_summary(response_body: dict, model_id: str) -> Dict[str, Any]:
    """Extract and format usage summary from a Bedrock response.

    Args:
        response_body: Parsed Bedrock response JSON.
        model_id: Model identifier.

    Returns:
        Usage summary dict with token counts and cost estimate.
    """
    usage = response_body.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)

    pricing = BEDROCK_MODEL_PRICING.get(model_id, {"input": 0, "output": 0})
    estimated_cost = (
        (input_tokens / 1_000_000) * pricing["input"]
        + (output_tokens / 1_000_000) * pricing["output"]
    )

    return {
        "model_id": model_id,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "estimated_cost_usd": round(estimated_cost, 6),
    }


if __name__ == "__main__":
    result = invoke_and_collect_metadata(
        prompt="What is machine learning?",
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    )
    print(json.dumps(result, indent=2))
