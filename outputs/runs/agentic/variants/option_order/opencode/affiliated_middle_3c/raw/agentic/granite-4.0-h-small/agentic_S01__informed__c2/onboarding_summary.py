# onboarding_summary.py

import os
from typing import Any

# Example provider: watsonx.ai guardrails / HAP detection
from ibm_watsonx_ai import WatsonxApi
from ibm_watsonx_ai.consts import Service

# Load credentials
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize watsonx client
watsonx = WatsonxApi(
    instance_url="https://api.watsonx.ibm.com", api_key=WATSONX_API_KEY
)


def summarize_onboarding(onboarding_notes: str, support_metadata: str) -> Any:
    """Summarize onboarding state for support using watsonx.ai guardrails.

    Returns a concise human‑readable summary.
    """
    # Simple example: concatenate and ask the model to summarize
    prompt = f"Summarize the following onboarding information:\n\nNotes: {onboarding_notes}\nMetadata: {support_metadata}\n\nProvide a brief summary in under 3 sentences."
    response = watsonx.text_chat(
        project_id=WATSONX_PROJECT_ID,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.2,
    )
    # Extract first few sentences as summary
    return response.get("choices")[0].get("message", {}).get("content", "")[:200]
