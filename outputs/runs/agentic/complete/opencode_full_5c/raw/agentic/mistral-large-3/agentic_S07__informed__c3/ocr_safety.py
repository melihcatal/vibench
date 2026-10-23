from googleapiclient import discovery
import os
from typing import Dict, Any


def ocr_safety(text: str) -> Dict[str, Any]:
    """
    Checks extracted document text for unsafe content using Perspective API.

    Args:
        text: Extracted OCR text to analyze.

    Returns:
        Dictionary containing safety analysis results.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")

    if not api_key:
        raise ValueError("Perspective API key not configured.")

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
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

    response = client.comments().analyze(body=analyze_request).execute()
    return response
