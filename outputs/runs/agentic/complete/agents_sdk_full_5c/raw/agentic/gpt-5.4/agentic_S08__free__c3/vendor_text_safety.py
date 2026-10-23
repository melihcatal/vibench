from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


class VendorTextSafetyModerator:
    def __init__(self, client: OpenAI | None = None):
        self.client = client or OpenAI()

    def moderate(self, vendor_notes: str) -> Dict[str, Any]:
        response = self.client.moderations.create(
            model=OPENAI_MODERATION_MODEL,
            input=vendor_notes,
        )
        result = response.results[0]
        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories),
            "category_scores": result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores),
            "provider": "openai",
            "model": OPENAI_MODERATION_MODEL,
        }
