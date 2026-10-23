from __future__ import annotations

import os
from typing import Any, Dict

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
DEFAULT_PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "THREAT",
    "PROFANITY",
    "IDENTITY_ATTACK",
]


def get_perspective_api_key() -> str:
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "").strip()
    if not api_key:
        raise ValueError("Missing PERSPECTIVE_API_KEY")
    return api_key


def get_default_thresholds() -> Dict[str, float]:
    return {
        "toxicity": 0.75,
        "severe_toxicity": 0.6,
        "insult": 0.8,
        "threat": 0.5,
        "profanity": 0.85,
        "identity_attack": 0.7,
    }


def build_requested_attributes(
    attributes: list[str] | None = None,
) -> Dict[str, Dict[str, Any]]:
    names = attributes or DEFAULT_PERSPECTIVE_ATTRIBUTES
    return {name: {} for name in names}


def perspective_analyze(
    text: str,
    *,
    attributes: list[str] | None = None,
    language: str | None = None,
    do_not_store: bool = True,
    session: requests.Session | None = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    api_key = get_perspective_api_key()
    payload: Dict[str, Any] = {
        "comment": {"text": text},
        "requestedAttributes": build_requested_attributes(attributes),
        "doNotStore": do_not_store,
    }
    if language:
        payload["languages"] = [language]
    http = session or requests.Session()
    response = http.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def extract_perspective_scores(result: Dict[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    attribute_scores = result.get("attributeScores", {})
    for attribute_name, payload in attribute_scores.items():
        summary = payload.get("summaryScore", {})
        value = summary.get("value", 0.0)
        scores[attribute_name.lower()] = float(value)
    return scores
