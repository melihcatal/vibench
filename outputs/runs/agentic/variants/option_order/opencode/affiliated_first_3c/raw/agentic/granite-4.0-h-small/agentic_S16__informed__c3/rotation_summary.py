# rotation_summary.py
# [LATER-STEP]
# Summarize secret rotation status using Granite via watsonx.ai

import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.consts import GraniteChatModel
from ibm_watsonx_ai.nlp import RetrievalAugmentedGeneration
from typing import Dict, Any


def summarize_rotation(secret_name: str, rotation_status: Dict[str, Any]) -> str:
    """Generate a concise summary of a secret rotation activity using Granite model via watsonx.ai.

    Args:
        secret_name: Name of the secret that was rotated.
        rotation_status: Dictionary containing rotation metadata (e.g., attempted_versions, success).

    Returns:
        A human‑readable summary text.
    """
    # Retrieve API credentials from environment
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables"
        )

    # Initialize Granite client (text generation)
    client = APIClient(api_key=api_key, project_id=project_id)
    model = GraniteChatModel.GRANITE_4_0_INSTRUCT_H

    # Prepare prompt for the model
    prompt = f"You are a concise technical writer. Summarize the secret rotation for secret '{secret_name}'.\n\nRotation metadata:\n{json.dumps(rotation_status, indent=2)}\n\nProvide a brief (1‑2 sentence) English summary that includes the rotation outcome and any notable details."

    # Call Granite for generation
    response = client.llm.generate_content(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.2,
    )
    # response.choices[0].message.content holds the generated text
    return response.choices[0].message.content.strip()
