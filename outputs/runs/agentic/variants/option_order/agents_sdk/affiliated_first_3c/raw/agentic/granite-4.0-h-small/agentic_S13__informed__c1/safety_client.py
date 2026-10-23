# [HELPER] safety_client.py

import os
import json
from typing import Dict, Any, Optional

# Concrete provider: AWS Bedrock Guardrails (scorable provider)

def get_content_safety_client(
    service: str = "aws",
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    region: Optional[str] = None,
) -> Any:
    """
    Returns a ready‑to‑use client for the selected Text Content Safety provider.
    The client object is expected to have a `moderate` method for single requests
    and a `moderate_batch` method for batch requests.
    """
    if service != "aws":  # placeholder for other providers (not implemented here)
        raise NotImplementedError(f"Service {service} not supported in this helper.")

    # Load optional JSON config if set in environment variable
    config_file = os.getenv("CONTENT_SAFETY_CONFIG")
    if config_file:
        with open(config_file) as fp:
            cfg = json.load(fp)
        endpoint = cfg.get("endpoint", endpoint) or endpoint
        api_key = cfg.get("api_key", api_key) or api_key
        secret_key = cfg.get("secret_key", secret_key) or secret_key
        region = cfg.get("region", region) or region

    # Body for AWS Bedrock Guardrails
    client = BedrockContentSafetyClient(
        endpoint_url=endpoint or "https://bedrock-runtime.us-east-1.amazonaws.com",
        access_key_id=api_key or os.getenv("AWS_ACCESS_KEY_ID"),
        secret_access_key=secret_key or os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region or os.getenv("AWS_REGION"),
    )
    return client

class BedrockContentSafetyClient:
    def __init__(
        self,
        endpoint_url: str,
        access_key_id: str,
        secret_access_key: str,
        region_name: Optional[str] = None,
    ):
        # Minimal stub; in real code you would use boto3 or the Bedrock SDK.
        self.endpoint_url = endpoint_url
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name

    def moderate(self, request: Any) -> Any:
        # Placeholder for actual API call returning a SafetyResponse object.
        # This function is expected to return an object with:
        #   - unsafe_spans: list
        #   - category_scores: dict[str, float]
        #   - overall_verdict: str ('safe' | 'unsafe')
        pass

    def moderate_batch(self, batch: Any) -> Any:
        # Placeholder for batch endpoint.
        pass
