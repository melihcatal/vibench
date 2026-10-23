import os
import requests
from typing import Dict
from document_models import SafetyResult
from document_client import get_perspective_client


def moderate_vendor_text(text: str) -> SafetyResult:
    """
    Moderates vendor notes or memo fields using Perspective API.
    """
    api_key = get_perspective_client()
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "doNotStore": True,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        result = response.json()

        scores = {}
        is_safe = True
        for attribute, value in result.get("attributeScores", {}).items():
            score = value["summaryScore"]["value"]
            scores[attribute] = score
            # A simple threshold for safety. Adjust as needed.
            if score > 0.7:  # If any score is above 0.7, consider it potentially unsafe
                is_safe = False

        message = "Text is safe." if is_safe else "Text may contain unsafe content."

        return SafetyResult(is_safe=is_safe, scores=scores, message=message)

    except requests.exceptions.RequestException as e:
        return SafetyResult(
            is_safe=False, message=f"Error calling Perspective API: {e}", scores={}
        )
