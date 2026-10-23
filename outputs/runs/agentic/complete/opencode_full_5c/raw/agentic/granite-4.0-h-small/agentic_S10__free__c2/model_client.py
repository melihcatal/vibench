# model_client.py
# [HELPER]
"""Local configuration and client utilities for hosted LLM inference.

This module provides a generic wrapper around a concrete hosted LLM
provider (OpenAI) and supplies helpers for model-family selection.
"""

import os
import json
from typing import Any, Dict, List

# Example concrete provider configuration (OpenAI API)
# Replace with your own API key or environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "demo_key")


class LLMClient:
    """High-level client for interacting with a hosted LLM provider.

    The client automatically selects the requested model family and
    handles request/response normalization.
    """

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        self.api_key = OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"

    def _make_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(self, messages: List[Any]) -> Dict:
        """Sends a chat completion request and returns normalized JSON payload.

        Args:
            messages (List[Any]): List of message dicts (role and content).
        Returns:
            dict: Normalized response containing `choices` list.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        response = self._request("/chat/completions", json=payload)
        return response

    def chat_stream(self, messages: List[Any]) -> Any:
        """Streams chat completion tokens in real time.

        Args:
            messages (List[Any]): List of message dicts.
        Yields:
            dict: Intermediate responses with `choices` and streaming deltas.
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }
        return self._request("/chat/completions", json=payload, stream=True)

    def _request(
        self, endpoint: str, *, json: Any = None, stream: bool = False
    ) -> Dict:
        """Performs a raw HTTP request to the OpenAI API.

        Args:
            endpoint (str): API endpoint to call.
            json (Any): JSON payload to send.
            stream (bool): Whether to enable streaming response.
        Returns:
            dict: Parsed JSON response.
        """
        import requests

        url = f"{self.base_url}{endpoint}"
        headers = self._make_headers()
        if stream:
            resp = requests.post(url, headers=headers, json=json, stream=True)
            # Yield each line from the response stream as JSON objects
            for line in resp.iter_lines():
                if line:
                    yield json.loads(line)
        else:
            resp = requests.post(url, headers=headers, json=json)
            resp.raise_for_status()
            return resp.json()
