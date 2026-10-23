from __future__ import annotations

from typing import Any, List, Dict


class Config:
    """Local configuration for Text Content Safety calls."""

    PROVIDER = "PERSPECTIVE_API"  # choose from the same-scenario list
    # If needed, add provider-specific settings (e.g., endpoint, model ID)


class ModerationRequest:
    """Normalize incoming text or batch into provider-specific payload."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.payload = self._build_payload()

    def _build_payload(self) -> dict:
        if Config.PROVIDER == "PERSPECTIVE_API":
            return {
                "comment": {"text": self.text},
                "requestedAttributes": {"TOXICITY": {}},
            }
        # Add other provider payload builders here
        raise ValueError(f"Unsupported provider: {Config.PROVIDER}")


class ModerationResponse:
    """Parse provider response into a unified format."""

    def __init__(self, provider_response: dict) -> None:
        self.provider_response = provider_response
        self._extract()

    def _extract(self) -> None:
        if Config.PROVIDER == "PERSPECTIVE_API":
            self.scores = {
                k: v["summaryScore"]["value"]
                for k, v in (
                    self.provider_response.get("attributeScores", {}) or {}
                ).items()
            }
        # Extend for other providers as needed


class Denormalizer:
    """Turn unified response into higher‑level decision data."""

    @staticmethod
    def to_decision(response: ModerationResponse) -> Dict[str, Any]:
        decision = {
            "text": response.provider_response.get("comment", {}).get("text"),
            "toxicity_score": response.scores.get("TOXICITY"),
        }
        return decision


# -------------------------------------------------
# Helper utilities (can be imported by later‑step files)
# -------------------------------------------------


def create_request(text: str) -> ModerationRequest:
    return ModerationRequest(text)


def parse_response(raw: dict) -> ModerationResponse:
    return ModerationResponse(raw)
