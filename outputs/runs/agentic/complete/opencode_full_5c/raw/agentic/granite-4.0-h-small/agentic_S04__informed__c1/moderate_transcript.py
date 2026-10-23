import os
import requests
from typing import List


def moderate_transcript(segments: List[str]) -> List[str]:
    """Moderate transcript text using Perspective API.

    Args:
        segments: List of text chunks from a transcript.

    Returns:
        List of cleaned segments where toxic content is replaced with [REDACTED].
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing PERSPECTIVE_API_KEY environment variable")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"Content-Type": "application/json"}
    cleaned_segments = []
    for seg in segments:
        data = {
            "comment": {
                "text": seg,
            },
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
            },
        }
        resp = requests.post(url, headers=headers, json=data, params={"key": api_key})
        result = resp.json()
        score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        if score >= 0.8:  # Threshold for strong toxicity
            cleaned_segments.append("[REDACTED]")
        else:
            cleaned_segments.append(seg)
    return cleaned_segments
