import os
import requests
from typing import List, Dict


def moderate_transcript(
    transcript_segments: List[Dict[str, str]],
) -> List[Dict[str, any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    moderated_segments = []

    for segment in transcript_segments:
        payload = {
            "comment": {"text": segment["text"]},
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
        params = {"key": api_key}
        response = requests.post(url, json=payload, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to moderate segment: {response.text}")
        moderated_segments.append(
            {**segment, "moderation": response.json()["attributeScores"]}
        )
    return moderated_segments
