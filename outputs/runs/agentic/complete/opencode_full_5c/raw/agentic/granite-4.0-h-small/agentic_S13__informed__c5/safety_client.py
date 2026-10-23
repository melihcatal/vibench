# safety_client.py

import os
from ibm_watsonx_ai.hlp import HlpClient  # concrete watsonx guardrails SDK (python)
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider identifiers (make the provider identifiable in code)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Helper utilities


def _create_auth() -> IAMAuthenticator:
    """Create an IAM authenticator for watsonx APIs."""
    return IAMAuthenticator(apikey=WATSONX_API_KEY)


def get_safety_client(timeout: int = 30) -> HlpClient:
    """Return a configured watsonx guardrails client ready for text safety calls."""
    authenticator = _create_auth()
    return HlpClient(
        authenticator=authenticator,
        service_url="https://api.us-south.watsonx.ibm.com",
        project_id=WATSONX_PROJECT_ID,
        timeout=timeout,
    )
