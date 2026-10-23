# [LATER-STEP] platform_output_safety.py
# Check watsonx.ai model output for unsafe content using guardrails

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import WATSONX_API_KEY, WATSONX_PROJECT_ID
from ibm_watsonx_ai.services import ContentModeration
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Dict, Any


def check_safety(model_output: str, deployment_id: str) -> bool:
    """Return True if the generated text passes watsonx guardrails, else False."""
    api_key = os.getenv(WATSONX_API_KEY)
    project_id = os.getenv(WATSONX_PROJECT_ID)
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    authenticator = IAMAuthenticator(api_key)
    client = APIClient(authenticator=authenticator, project_id=project_id)
    moderation = ContentModeration(client)

    # watsonx guardrails endpoint expects raw text and optional deployment id
    response = moderation.analyze_content(
        content=model_output,
        deployment_id=deployment_id,  # optional; helps context‑aware detection
    )

    # The response contains a 'safe' boolean field (or similar)
    # Exact field name may vary; adapt to actual SDK response shape
    is_safe = response.get("safe", False)
    return is_safe
