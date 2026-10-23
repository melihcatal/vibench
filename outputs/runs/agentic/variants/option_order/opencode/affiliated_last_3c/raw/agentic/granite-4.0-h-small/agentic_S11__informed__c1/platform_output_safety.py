import json
import os
from urllib.parse import urlencode
import requests
from typing import Dict, Any


class ProviderConfig:
    """Centralized configuration for the text‑content‑safety provider.

    Environment variables are used; missing variables raise an error.
    """

    # Azure AI Content Safety (recommended for Realtime scenarios)
    ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    API_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    # Optional: if you prefer the generic Azure OpenAI Content Safety endpoint
    OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

    @classmethod
    def validate(cls):
        """Ensure required credentials are present."""
        missing = []
        if not cls.ENDPOINT:
            missing.append("AZURE_CONTENT_SAFETY_ENDPOINT")
        if not cls.API_KEY:
            missing.append("AZURE_CONTENT_SAFETY_KEY")
        if missing:
            raise RuntimeError(
                f"Missing Azure Content Safety credentials: {', '.join(missing)}"
            )


class ContentSafetyClient:
    """Thin wrapper around Azure AI Content Safety REST API for toxicity/unsafe detection.

    The client follows the documentation at https://learn.microsoft.com/azure/ai-content-safety/quickstart
    """

    PROVIDER = "Azure AI Content Safety"
    API_PATH = "/v1.0/text/moderations/content"

    def __init__(self):
        ProviderConfig.validate()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "api-key": ProviderConfig.API_KEY,
            }
        )
        # Base URL can be Azure OpenAI or dedicated Content Safety endpoint
        if ProviderConfig.ENDPOINT:
            self.base_url = ProviderConfig.ENDPOINT.rstrip("/") + self.API_PATH
        else:
            # Fallback to Azure OpenAI content safety route
            self.base_url = (
                ProviderConfig.OPENAI_ENDPOINT.rstrip("/")
                + "/contentSafety/text/moderations"
            )

    def evaluate(self, text: str) -> Dict[str, Any]:
        """Run moderation on the supplied text.

        Returns the JSON payload returned by the service.
        """
        payload = {
            "input": {
                "type": "text",
                "text": text,
            },
            # optional parameters – adjust as needed
            "properties": {
                "rating": "safe",
                "categoryId": ["toxicity", "hate", "self_harm", "sexual", "violence"],
            },
        }
        resp = self.session.post(self.base_url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()


def check_unsafe(
    model_output: str,
) -> bool:
    """Return True if the provider flags `model_output` as unsafe content.

    The function abstracts the concrete provider; callers can rely on the binary
    result without knowing implementation details.
    """
    client = ContentSafetyClient()
    result = client.evaluate(model_output)
    # Azure Content Safety returns a list of moderation categories with scores.
    # We consider the content unsafe if any category score exceeds the default threshold (0.5).
    categories = result.get("categories", [])
    for cat in categories:
        if cat.get("score", 0.0) > 0.5:
            return True
    return False


# ----------------------------------------------------------------------
# Example usage for a quick sanity check (not executed by default)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     text = "This is a harmless sentence."
#     print(check_unsafe(text))  # Expected output: False
