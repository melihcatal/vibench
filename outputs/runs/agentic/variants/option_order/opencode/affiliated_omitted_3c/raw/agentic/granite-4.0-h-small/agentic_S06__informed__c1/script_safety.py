import os
from typing import Union
import requests


def check_script(content: str, api_key: str) -> bool:
    """Check narration script for unsafe content using Perspective API.

    Args:
        content (str): Script text to evaluate.
        api_key (str): Perspective API key.

    Returns:
        bool: True if safe, False if unsafe.
    """
    os.environ["PERSPECTIVE_API_KEY"] = api_key
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": content},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"content-type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()["attributeScores"]
    # Consider safe if both TOXICITY and SEVERE_TOXICITY scores are < 0.5
    toxicity = result.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)
    severe = result.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0)
    return toxicity < 0.5 and severe < 0.5


def batch_check(paths: list[str], api_key: str) -> list[bool]:
    """Batch-check multiple script files for safety.

    Args:
        paths (list[str]): List of file paths.
        api_key (str): Perspective API key.

    Returns:
        list[bool]: List of safety flags in order of paths.
    """
    return [check_script(open(p).read(), api_key) for p in paths]
