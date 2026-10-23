from __future__ import annotations

import os
from typing import Any

import requests

from safety_models import (
    CategoryScore,
    ModerationRequest,
    ModerationResult,
    normalize_text,
)


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "IDENTITY_ATTACK",
]


def get_perspective_api_key() -> str:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY is empty")
    return api_key


def build_perspective_payload(request: ModerationRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "comment": {"text": normalize_text(request.text)},
        "requestedAttributes": {name: {} for name in PERSPECTIVE_ATTRIBUTES},
        "doNotStore": True,
    }
    if request.language:
        payload["languages"] = [request.language]
    if request.user_id:
        payload["clientToken"] = request.user_id
    return payload


def call_perspective(payload: dict[str, Any], timeout: float = 15.0) -> dict[str, Any]:
    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": get_perspective_api_key()},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def parse_perspective_result(
    text: str,
    response: dict[str, Any],
    threshold: float = 0.7,
) -> ModerationResult:
    attribute_scores = response.get("attributeScores", {})
    categories: dict[str, CategoryScore] = {}
    blocked = False
    for name, payload in attribute_scores.items():
        value = float(payload["summaryScore"]["value"])
        flagged = value >= threshold
        blocked = blocked or flagged
        categories[name.lower()] = CategoryScore(
            name=name.lower(), score=value, flagged=flagged
        )
    action = "block" if blocked else "allow"
    return ModerationResult(
        text=text,
        action=action,
        blocked=blocked,
        categories=categories,
        provider="Perspective API",
        raw=response,
    )


def moderate_text_request(
    request: ModerationRequest,
    threshold: float = 0.7,
) -> ModerationResult:
    payload = build_perspective_payload(request)
    response = call_perspective(payload)
    return parse_perspective_result(request.text, response, threshold=threshold)
