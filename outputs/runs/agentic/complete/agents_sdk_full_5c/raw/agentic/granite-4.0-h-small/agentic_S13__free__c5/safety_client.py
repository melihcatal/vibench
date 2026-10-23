import os
from typing import Any, Dict

# Example: using OpenAI's moderation endpoint via the openai Python SDK
import openai

class SafetyClient:
    """Thin wrapper around the OpenAI moderation endpoint for text safety checks."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OpenAI API key not provided. Set environment variable OPENAI_API_KEY.")
        openai.api_key = self.api_key

    def moderate(self, text: str) -> Dict[str, Any]:
        """Call OpenAI moderation moderation endpoint for a single text.

        Returns a dict compatible with our helper expectations:
            {
                \"flagged\": bool,
                \"categories\": { \"harassment\": bool, \"self-harm\": bool, ... }
            }
        """
        response = openai.Moderation.create(input=text)
        # The official response includes a list of results; we flatten to a single dict.
        result = response["results"][0]
        return {
            "flagged": result["flagged"],
            "categories": {cat["category_name"]: cat["flagged"] for cat in result.get("categories", [])},
        }

    def moderate_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        """Batch moderation using the same endpoint.

        Returns a list of dicts as produced by moderate().
        """
        responses = openai.Moderation.create(input=texts)
        # The OpenAI API accepts a list and returns a list of results.
        return [
            {
                "flagged": r["flagged"],
                "categories": {cat["category_name"]: cat["flagged"] for cat in r.get("categories", [])},
            }
            for r in responses["results"]
        ]
