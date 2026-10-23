import os
import requests


def check_prompt_safety(prompt: str, generated_text: str = "") -> dict:
    """
    Check prompts and generated text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Combine prompt and generated text for analysis
    text_to_analyze = f"{prompt}\n\n{generated_text}".strip()

    params = {"key": api_key}

    data = {
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

    response = requests.post(url, params=params, json=data)
    response.raise_for_status()

    result = response.json()

    # Extract scores
    scores = {}
    for attribute_name, attribute_data in result.get("attributeScores", {}).items():
        scores[attribute_name.lower()] = attribute_data.get("summaryScore", {}).get(
            "value", 0
        )

    # Determine overall safety
    is_safe = all(score < 0.7 for score in scores.values())

    return {
        "is_safe": is_safe,
        "scores": scores,
        "text_analyzed": text_to_analyze[:500],  # Truncate for response
    }
