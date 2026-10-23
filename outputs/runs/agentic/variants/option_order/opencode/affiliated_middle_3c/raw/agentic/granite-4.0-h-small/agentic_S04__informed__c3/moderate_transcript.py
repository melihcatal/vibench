import os
import requests
from speech_client import get_speech_client


def moderate_transcript(transcript, api_key=os.getenv("PERSPECTIVE_API_KEY")):
    """Run toxic content moderation on a transcript using Perspective API.

    Parameters
    ----------
    transcript : str
        Transcript text to evaluate.
    api_key : str, optional
        API key for Perspective; defaults to env var PERSPECTIVE_API_KEY.

    Returns
    -------
    dict
        Moderation scores, e.g., 'toxicity' and 'severe_toxicity'.
    """
    if not api_key:
        raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": transcript},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"x-api-key": api_key}
    resp = requests.post(endpoint, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]
    # Return simplified scores
    return {k: v["summaryScore"]["value"] for k, v in scores.items()}
