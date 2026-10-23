import os
import json
from ibm_watsonx_ai.nlp import ContentSafetyClient
from ibm_watsonx_ai import APIClient


def secret_label_safety(secret_id: str, secret_version: str = "latest") -> dict:
    """Check secret labels and notes for unsafe text using watsonx guardrails."""
    from security_client import SecretsClient
    client = SecretsClient()
    payload = client.get_secret(secret_id, secret_version)
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError("Missing WATSONX_API_KEY or WATSONX_PROJECT_ID")
    # Use the guardrails endpoint via the nlp client
    client = APIClient(authenticator=APIClient.ApiKeyAuthenticator(api_key))
    guardrails = ContentSafetyClient(authenticator=APIClient.ApiKeyAuthenticator(api_key), project_id=project_id, url="https://api.us-south.watsonx.ai/v1")
    unsafe = guardrails.check_text(text=json.dumps(payload))
    return {
        "secret_id": secret_id,
        "version": secret_version,
        "unsafe": unsafe.get_result()
    }
