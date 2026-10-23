from typing import List
import requests
import os


def check_text_safety(texts: List[str]) -> Dict[str, Any]:
    """
    Checks corpus texts for safety using Perspective API before embedding.

    Args:
        texts: List of input texts to check for safety.

    Returns:
        Dict[str, Any]: Safety analysis results for each text.

    Raises:
        ValueError: If the PERSPECTIVE_API_KEY environment variable is not set.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []

    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "languages": ["en"],
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        results.append(response.json())

    return {"texts": texts, "safety_results": results}
