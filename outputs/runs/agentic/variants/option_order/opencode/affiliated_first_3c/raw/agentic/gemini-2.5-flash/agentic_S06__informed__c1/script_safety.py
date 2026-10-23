import requests
import os
from speech_client import PerspectiveAPIClient
from speech_models import AnalyzeTextRequest, AnalyzeTextResponse


def check_script_safety(
    text: str, attribute_thresholds: dict = None
) -> AnalyzeTextResponse:
    """
    Checks narration scripts for unsafe content using Perspective API.
    """
    client_wrapper = PerspectiveAPIClient()
    api_key = client_wrapper.api_key
    base_url = client_wrapper.base_url

    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    if attribute_thresholds is None:
        attribute_thresholds = {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        }

    requested_attributes = {attr: {} for attr in attribute_thresholds.keys()}

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "doNotStore": True,
    }

    params = {"key": api_key}

    try:
        response = requests.post(base_url, params=params, json=payload)
        response.raise_for_status()
        result = response.json()

        attribute_scores = {}
        if "attributeScores" in result:
            for attr, scores in result["attributeScores"].items():
                attribute_scores[attr] = scores["summaryScore"]["value"]

        return AnalyzeTextResponse(attribute_scores=attribute_scores)
    except requests.exceptions.RequestException as e:
        print(f"Error checking script safety with Perspective API: {e}")
        return AnalyzeTextResponse(attribute_scores={})
