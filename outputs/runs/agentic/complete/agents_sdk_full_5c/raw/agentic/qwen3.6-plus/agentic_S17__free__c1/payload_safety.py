"""
payload_safety.py - Checks decrypted text payloads for unsafe content using AWS Bedrock.

Uses Amazon Bedrock with the Anthropic Claude model (anthropic.claude-3-sonnet-20240229-v1:0)
to analyze decrypted text payloads for unsafe content including PII, credentials,
injection patterns, and other security concerns.

Provider: Amazon Bedrock (bedrock.us-east-1.amazonaws.com)
Model ID: anthropic.claude-3-sonnet-20240229-v1:0
"""

import json
import logging
import sys
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config

from security_models import PayloadSafetyResult

logger = logging.getLogger(__name__)

REGION = "us-east-1"
SAFETY_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

SAFETY_PROMPT_TEMPLATE = """You are a security analysis assistant. Analyze the following decrypted text payload for safety and security concerns.

Check for:
1. Personally Identifiable Information (PII) - SSNs, email addresses, phone numbers, physical addresses
2. Credentials and secrets - API keys, passwords, tokens, connection strings
3. Injection patterns - SQL injection, XSS, command injection, path traversal
4. Malicious content - malware indicators, obfuscated code, encoded payloads
5. Policy violations - unauthorized data, restricted content, compliance concerns

Payload to analyze:
---
{text}
---

Respond with ONLY a JSON object in this exact format (no markdown, no extra text):
{{
  "is_safe": true or false,
  "flags": ["list", "of", "identified", "issues"],
  "severity": "low" | "medium" | "high" | "critical",
  "details": {{
    "pii_found": true or false,
    "credentials_found": true or false,
    "injection_patterns_found": true or false,
    "malicious_content_found": true or false,
    "policy_violations_found": true or false,
    "description": "brief explanation of findings"
  }}
}}"""


def get_bedrock_runtime_client(region: str = REGION) -> boto3.client:
    """
    Initialize an Amazon Bedrock Runtime client via boto3.
    Endpoint: bedrock-runtime.us-east-1.amazonaws.com
    """
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        region_name=region,
    )
    return boto3.client("bedrock-runtime", config=config)


def invoke_bedrock_safety_check(
    payload_text: str,
    model_id: str = SAFETY_MODEL_ID,
    region: str = REGION,
    max_tokens: int = 1024,
    temperature: float = 0.0,
) -> Dict[str, Any]:
    """
    Invoke Amazon Bedrock with Anthropic Claude to analyze payload safety.

    Uses the Converse API to send the safety analysis prompt and parse the JSON response.

    Args:
        payload_text: The decrypted text payload to analyze.
        model_id: Bedrock model ID (default: anthropic.claude-3-sonnet-20240229-v1:0).
        region: AWS region for Bedrock.
        max_tokens: Maximum tokens in response.
        temperature: Sampling temperature (0.0 for deterministic output).

    Returns:
        Parsed JSON dict with safety analysis results.

    Raises:
        RuntimeError: If Bedrock invocation fails.
    """
    client = get_bedrock_runtime_client(region)

    prompt = SAFETY_PROMPT_TEMPLATE.format(text=payload_text)

    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    inference_config = {
        "maxTokens": max_tokens,
        "temperature": temperature,
    }

    try:
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig=inference_config,
        )

        output_text = response["output"]["message"]["content"][0]["text"]

        # Extract JSON from response (may have markdown code blocks)
        json_str = output_text.strip()
        if json_str.startswith("```"):
            json_str = json_str.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]
        json_str = json_str.strip()

        result = json.loads(json_str)
        return result

    except Exception as e:
        raise RuntimeError(
            f"Amazon Bedrock safety analysis failed with model {model_id}: {e}"
        ) from e


def check_payload_safety(
    payload_text: str,
    model_id: str = SAFETY_MODEL_ID,
    region: str = REGION,
) -> PayloadSafetyResult:
    """
    Check a decrypted text payload for unsafe content using Amazon Bedrock.

    Args:
        payload_text: The decrypted plaintext to analyze.
        model_id: Bedrock model ID.
        region: AWS region.

    Returns:
        PayloadSafetyResult with safety verdict, flags, severity, and details.

    Raises:
        RuntimeError: If safety analysis fails.
    """
    raw_result = invoke_bedrock_safety_check(payload_text, model_id=model_id, region=region)

    is_safe = raw_result.get("is_safe", True)
    flags = raw_result.get("flags", [])
    severity = raw_result.get("severity", "low")
    details = raw_result.get("details", {})

    result = PayloadSafetyResult(
        text=payload_text,
        is_safe=is_safe,
        flags=flags if isinstance(flags, list) else [flags],
        severity=severity,
        details=details,
    )

    logger.info(
        "Payload safety check: is_safe=%s, severity=%s, flags=%s",
        result.is_safe,
        result.severity,
        result.flags,
    )
    return result


def main():
    """CLI entry point for payload_safety."""
    if len(sys.argv) < 2:
        print("Usage: python payload_safety.py <payload_text>")
        sys.exit(1)

    payload_text = sys.argv[1]

    logging.basicConfig(level=logging.INFO)
    result = check_payload_safety(payload_text)

    output = {
        "is_safe": result.is_safe,
        "severity": result.severity,
        "flags": result.flags,
        "details": result.details,
        "text_preview": result.text[:200] + "..." if len(result.text) > 200 else result.text,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
