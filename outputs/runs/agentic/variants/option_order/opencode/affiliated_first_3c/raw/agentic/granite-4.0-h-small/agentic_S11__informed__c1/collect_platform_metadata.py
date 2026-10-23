# [SAME-SCENARIO] collect_platform_metadata.py
# Return model output together with watsonx.ai platform metadata

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import WATSONX_API_KEY, WATSONX_PROJECT_ID
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Dict, Any


def collect_metadata(deployment_id: str, prompt: str) -> Dict[str, Any]:
    """Invoke a model and attach usage, request, and resource metadata."""
    api_key = os.getenv(WATSONX_API_KEY)
    project_id = os.getenv(WATSONX_PROJECT_ID)
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    # Set up authenticator required by certain endpoints (e.g., usage API)
    authenticator = IAMAuthenticator(api_key)
    client = APIClient(authenticator=authenticator, project_id=project_id)

    # 1. Invoke the model (re-use invoke_model logic for consistency)
    invoke_resp = client.text_generation.complete(
        deployment_name=f"{deployment_id}---text-completion",
        messages=[{"content": prompt}],
        max_tokens=256,
    )
    output_text = invoke_resp.get_result()

    # 2. Pull usage metrics for this request (if the service provides it)
    usage = (
        client.usage.get_usage()
    )  # returns overall usage, you can target specific deployment later

    metadata = {
        "provider": "watsonx.ai",
        "deployment_id": deployment_id,
        "output_text": output_text,
        "provider_metadata": {
            "usage_summary": usage.get_summary(),
            "request_id": invoke_resp.get_request_id(),
            # Example: fetch deployment details to include extra handles
            "deployment_info": client.deployments.get_by_id(
                invoke_resp.get_deployment_id()
            ),
        },
    }
    return metadata
