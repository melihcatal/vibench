import os
import requests


def message_safety(text: str) -> bool:
    """
    Checks message payload text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not found in environment variables.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    response_dict = response.json()

    toxicity_score = response_dict["attributeScores"]["TOXICITY"]["summaryScore"][
        "value"
    ]

    # Consider content unsafe if toxicity score is above 0.7
    return toxicity_score <= 0.7
