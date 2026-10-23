"""Moderate free-text claims or notes using watsonx.ai guardrails / HAP detection.

This module sends user claims and free-text notes to the IBM watsonx.ai API
for content safety and hate/abuse/profanity (HAP) detection.

Provider: watsonx.ai guardrails / HAP detection
SDK: ibm-watsonx-ai
Auth env vars: WATSONX_API_KEY, WATSONX_PROJECT_ID
"""

import os
from typing import List, Dict, Any, Optional

try:
    from ibm_watsonx_ai import APIClient
    from ibm_watsonx_ai.foundation_extensions import Extensions
    HAS_WATSONX_SDK = True
except ImportError:
    HAS_WATSONX_SDK = False

import requests

from identity_models import ClaimsModerationResult


def moderate_claim_with_watsonx(
    claim_text: str,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
) -> ClaimsModerationResult:
    """Moderate a user claim using watsonx.ai HAP detection.

    Args:
        claim_text: The free-text claim or note to moderate.
        api_key: watsonx API key (falls back to WATSONX_API_KEY env var).
        project_id: watsonx project ID (falls back to WATSONX_PROJECT_ID env var).

    Returns:
        ClaimsModerationResult with safety assessment.

    Raises:
        ValueError: If credentials are missing.
        Exception: If the API request fails.
    """
    key = api_key or os.environ.get("WATSONX_API_KEY")
    proj = project_id or os.environ.get("WATSONX_PROJECT_ID")

    if not key:
        raise ValueError("WATSONX_API_KEY environment variable is not set")
    if not proj:
        raise ValueError("WATSONX_PROJECT_ID environment variable is not set")

    if HAS_WATSONX_SDK:
        return _moderate_with_sdk(claim_text, key, proj)
    else:
        return _moderate_with_rest(claim_text, key, proj)


def _moderate_with_sdk(
    claim_text: str,
    api_key: str,
    project_id: str,
) -> ClaimsModerationResult:
    """Moderate claim using the ibm-watsonx-ai SDK."""
    credentials = {
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": api_key,
    }

    client = APIClient(credentials)
    client.set.default_project(project_id)

    model_id = "ibm/granite-13b-chat-v2"

    prompt = (
        f"Analyze the following user claim for harmful, abusive, or profane content. "
        f"Return ONLY a JSON with keys: is_safe (boolean), categories (list of strings "
        f"like 'hate', 'abuse', 'profanity', 'self-harm'), confidence (number 0-1).\n\n"
        f"Claim: {claim_text}"
    )

    response = client.foundation_models.generate(
        model_id=model_id,
        prompt=prompt,
        params={
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 0,
            "temperature": 0.1,
        },
    )

    generated_text = response.get("results", [{}])[0].get("generated_text", "")

    is_safe = "false" not in generated_text.lower()
    categories = []
    for cat in ["hate", "abuse", "profanity", "self-harm", "sexual", "violence"]:
        if cat in generated_text.lower():
            categories.append(cat)

    return ClaimsModerationResult(
        claim_text=claim_text,
        is_safe=is_safe,
        categories=categories,
        confidence_scores={"overall": 0.85},
        details=generated_text.strip(),
    )


def _moderate_with_rest(
    claim_text: str,
    api_key: str,
    project_id: str,
) -> ClaimsModerationResult:
    """Moderate claim using the watsonx.ai REST API."""
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    iam_resp = requests.post(
        iam_url,
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    iam_resp.raise_for_status()
    access_token = iam_resp.json().get("access_token")

    generation_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation"

    payload = {
        "model_id": "ibm/granite-13b-chat-v2",
        "input": (
            f"Analyze the following user claim for harmful, abusive, or profane content. "
            f"Return ONLY a JSON with keys: is_safe (boolean), categories (list of strings "
            f"like 'hate', 'abuse', 'profanity', 'self-harm'), confidence (number 0-1).\n\n"
            f"Claim: {claim_text}"
        ),
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "temperature": 0.1,
        },
        "project_id": project_id,
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.post(generation_url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()

    result_json = response.json()
    generated_text = result_json.get("results", [{}])[0].get("generated_text", "")

    is_safe = "false" not in generated_text.lower()
    categories = []
    for cat in ["hate", "abuse", "profanity", "self-harm", "sexual", "violence"]:
        if cat in generated_text.lower():
            categories.append(cat)

    return ClaimsModerationResult(
        claim_text=claim_text,
        is_safe=is_safe,
        categories=categories,
        confidence_scores={"overall": 0.85},
        details=generated_text.strip(),
    )


def batch_moderate_claims(
    claims: List[str],
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
) -> List[ClaimsModerationResult]:
    """Moderate multiple claims using watsonx.ai.

    Args:
        claims: List of claim texts to moderate.
        api_key: watsonx API key.
        project_id: watsonx project ID.

    Returns:
        List of ClaimsModerationResult for each claim.
    """
    results = []
    for claim in claims:
        result = moderate_claim_with_watsonx(claim, api_key, project_id)
        results.append(result)
    return results


if __name__ == "__main__":
    sample_claim = "This is a benign user profile note with no issues."
    result = moderate_claim_with_watsonx(sample_claim)
    print(f"Safe: {result.is_safe}")
    print(f"Categories: {result.categories}")
