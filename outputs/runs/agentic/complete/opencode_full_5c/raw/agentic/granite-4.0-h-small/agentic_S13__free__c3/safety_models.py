# [HELPER] safety_models.py
"""Define local request, response, and normalization helpers for Text Content Safety.
Aligns with OpenAI Moderation API contract.
"""


class ModerationRequest:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self) -> dict:
        """Convert to format expected by the provider."""
        return {"input": self.text}


class ModerationResponse:
    def __init__(self, data: dict):
        self._data = data

    @property
    def flagged(self) -> bool:
        """True if any category is flagged."""
        return self._data["results"][0]["flagged"]

    @property
    def categories(self) -> dict:
        """Map of category name to score."""
        result = self._data["results"][0]
        # Scores are stored under 'category_scores' in this example
        return result.get("category_scores", {})


# Simple normalization wrapper


def normalize_moderation_response(raw: dict) -> ModerationResponse:
    return ModerationResponse(raw)
