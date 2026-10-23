import os
import requests
from typing import Dict, Any


def check_prompt_safety(prompt: str, generated_text: str = "") -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Combine prompt and generated text for analysis
    text_to_analyze = (
        f"Prompt: {prompt}\nGenerated: {generated_text}" if generated_text else prompt
    )

    params = {"key": api_key}

    payload = {
        "comment": {"text": text_to_analyze},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()

    result = response.json()

    # Extract scores
    attribute_scores = result.get("attributeScores", {})
    scores = {}

    for attribute_name, attribute_data in attribute_scores.items():
        scores[attribute_name] = attribute_data.get("summaryScore", {}).get(
            "value", 0.0
        )

    # Determine overall safety
    max_score = max(scores.values()) if scores else 0.0
    is_safe = max_score < 0.7  # Threshold for safety

    return {
        "is_safe": is_safe,
        "scores": scores,
        "max_score": max_score,
        "flagged_attributes": [attr for attr, score in scores.items() if score >= 0.7],
    }
