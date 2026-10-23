import os

import requests

from safety_models import normalize_text, normalize_thresholds


PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]


def perspective_analyze(text, attributes, config=None):
    config = config or {}
    response = requests.post(
        PERSPECTIVE_HOST,
        params={"key": get_api_key(config)},
        json={
            "comment": {"text": normalize_text(text)},
            "languages": config.get("languages", ["en"]),
            "requestedAttributes": {name: {} for name in attributes},
            "doNotStore": True,
        },
        timeout=config.get("timeout", 30),
    )
    response.raise_for_status()
    return response.json()


def get_score(result, category):
    return float(result["attributeScores"][category]["summaryScore"]["value"])


def get_thresholds(config=None):
    config = config or {}
    return normalize_thresholds(config.get("thresholds"))
