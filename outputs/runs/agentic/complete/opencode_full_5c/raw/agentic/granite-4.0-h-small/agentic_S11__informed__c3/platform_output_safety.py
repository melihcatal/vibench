# platform_output_safety.py
# LATER-STEP: checks platform model output for unsafe content

import os
from model_client import get_provider_client
from model_models import parse_response


def run_safety_filter(output: str, raw: dict = None) -> dict:
    """Runs a safety analysis on model output and returns verdict details."""
    provider = infer_provider_name()
    if provider == "aws":
        # Example: Amazon Bedrock Guardrails API
        client = get_provider_client("aws")
        # Guardrails expects a text payload; real API may need request transformation
        safety_resp = client.detect_profanity(text=output)
        return {
            "provider": "bedrock",
            "service": "guardrails",
            "verdict": safety_resp.get("verdict"),
            "flags": safety_resp.get("flags"),
            "raw": safety_resp,
        }
    elif provider == "azure_openai":
        # Azure AI Content Safety REST endpoint (or SDK)
        client = get_provider_client("azure")
        safety_payload = {"text": output}
        safety_resp = client.analyze_content(safety_payload)
        return {
            "provider": "azure",
            "service": "contentsafety",
            "verdict": safety_resp.get("result"),
            "categories": safety_resp.get("categories"),
            "raw": safety_resp,
        }
    # Add other providers as needed
    return {"provider": provider, "verdict": "unknown"}
