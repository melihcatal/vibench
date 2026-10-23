import os
from typing import Literal


class ContentSafetyConfig:
    """Local helper for configuring a text safety provider.",
    Supports Anthropic via API key / endpoint.
    """

    def __init__(
        self,
        provider: Literal["anthropic"] = "anthropic",  # placeholder for provider
        **kwargs,
    ):
        self.provider = provider
        if provider == "anthropic":
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            self.endpoint = os.getenv(
                "ANTHROPIC_ENDPOINT", "https://api.anthropic.com/v1"
            )
        # Add additional providers if needed

    def get_client(self) -> object:
        """Return a configured client instance for the chosen provider.",
        Returns a dummy class for demonstration; replace with real SDK/client.
        """

        # Placeholder client implementation
        class DummyClient:
            def moderate(self, text: str) -> dict:
                # Mock moderation result
                return {
                    "decision": "safe",
                    "scores": {"toxicity": 0.1},
                    "unsafe_spans": [],
                }

            def moderate_batch(self, messages: list[str]) -> list[dict]:
                return [self.moderate(msg) for msg in messages]

        return DummyClient()


def get_safety_client() -> object:
    """Utility to instantiate a configured safety client.",
    Reads environment variables and returns a ready-to-use client.
    """
    cfg = ContentSafetyConfig()
    return cfg.get_client()
