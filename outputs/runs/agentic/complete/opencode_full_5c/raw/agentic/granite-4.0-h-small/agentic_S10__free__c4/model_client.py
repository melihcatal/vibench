import os
from typing import Any, Dict, Tuple

# Example provider - OpenAI (gpt-4o)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class HostedModelClient:
    def __init__(self, model: str = "gpt-4o") -> None:
        self.model = model
        # Configure authentication (e.g., API key) here
        self.headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        # Base URL for the provider's inference endpoint
        self.base_url = f"https://api.openai.com/v1/chat/completions"

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Generic POST request to the provider's API."""
        import requests

        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def chat_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for chat completions."""
        payload["model"] = self.model
        return self._post(payload)

    def chat_completion_stream(
        self, payload: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Any]:
        """Streaming capability for long responses (not implemented for the example)."""
        raise NotImplementedError("Streaming not implemented in this example client")
