from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional

import requests

from safety_models import ModerationDecision, ModerationRequest, TextSafetyConfig, clamp_score, normalize_text


@dataclass
class PerspectiveClient:
    config: TextSafetyConfig

    def moderate(self, request: ModerationRequest) -> ModerationDecision:
        payload = {
            "comment": {"text": normalize_text(request.text)},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "THREAT": {},
            },
            "doNotStore": True,
        }
        if request.language:
            payload["languages"] = [request.language]

        response = requests.post(
            self.config.endpoint,
            params={"key": self.config.api_key},
            json=payload,
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        attr = data.get("attributeScores", {})
        scores = {
            name.lower(): clamp_score(v.get("summaryScore", {}).get("value"))
            for name, v in attr.items()
        }
        flagged = any(score >= 0.5 for score in scores.values())
        return ModerationDecision(flagged=flagged, scores=scores, raw=data)


def load_config() -> TextSafetyConfig:
    api_key = os.environ["PERSPECTIVE_API_KEY"]
    endpoint = os.environ.get(
        "PERSPECTIVE_API_ENDPOINT",
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
    )
    timeout_seconds = int(os.environ.get("PERSPECTIVE_API_TIMEOUT_SECONDS", "30"))
    return TextSafetyConfig(api_key=api_key, endpoint=endpoint, timeout_seconds=timeout_seconds)


def get_client() -> PerspectiveClient:
    return PerspectiveClient(load_config())
