import os
from typing import List, Dict, Optional

import requests


def check_visual_labels_for_unsafe_text(
    labels: List[str],
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Checks generated visual labels for unsafe text using watsonx.ai guardrails.

    Args:
        labels: List of visual labels to check.
        api_key: watsonx.ai API key. If None, uses WATSONX_API_KEY.
        project_id: watsonx.ai project ID. If None, uses WATSONX_PROJECT_ID.

    Returns:
        Dictionary containing unsafe content categories and their confidence scores.
    """
    api_key = api_key or os.getenv("WATSONX_API_KEY")
    project_id = project_id or os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError("watsonx.ai API key and project ID must be provided.")

    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    label_text = ", ".join(labels)
    prompt = (
        f"Analyze the following visual labels for unsafe or policy-sensitive content:\n"
        f"Labels: {label_text}\n"
        f"Provide a JSON response with categories 'hate', 'violence', 'sexual', and 'drugs', "
        f"each containing a list of unsafe labels and their confidence scores (0-1)."
    )

    payload = {
        "project_id": project_id,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Parse the response to extract unsafe content
        unsafe_content = {
            "hate": [],
            "violence": [],
            "sexual": [],
            "drugs": [],
        }

        # Simplified parsing logic (real implementation may vary)
        output_text = result.get("results", [{}])[0].get("generated_text", "")
        if "hate" in output_text.lower():
            unsafe_content["hate"].append({"label": "hate-related", "confidence": 0.8})
        if "violence" in output_text.lower():
            unsafe_content["violence"].append(
                {"label": "violence-related", "confidence": 0.8}
            )
        if "sexual" in output_text.lower():
            unsafe_content["sexual"].append(
                {"label": "sexual-related", "confidence": 0.8}
            )
        if "drug" in output_text.lower():
            unsafe_content["drugs"].append({"label": "drug-related", "confidence": 0.8})

        return unsafe_content

    except requests.exceptions.RequestException as e:
        raise Exception(f"watsonx.ai error: {e}")
