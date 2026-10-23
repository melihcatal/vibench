import os
import json
import httpx


class HostedLLMClient:
    """Local helper client for calling a concrete hosted LLM provider (OpenAI)."""

    def __init__(self):
        # Provider-specific endpoint and auth loaded from environment variables
        self.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _request(self, endpoint: str, payload: dict) -> dict:
        """Internal helper to issue a POST request with JSON payload."""
        url = f"{self.api_base}{endpoint}"
        resp = httpx.post(url, headers=self.headers, json=payload, timeout=30.0)
        resp.raise_for_status()
        return resp.json()

    def generate(self, payload: dict) -> dict:
        """Calls the `/v1/chat/completions` endpoint for a completion."""
        return self._request("/v1/chat/completions", payload)

    def stream_generate(self, payload: dict):
        """Streams completion from `/v1/chat/completions` using streaming."""
        # Use the low-level HTTP streaming interface
        url = f"{self.api_base}/v1/chat/completions"

        async def _stream():
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST", url, headers=self.headers, json=payload, timeout=None
                ) as resp:
                    await resp.aread()  # Ensure connection established
                    async for line in resp.aiter_lines():
                        if line.startswith("[") or line.startswith("{"):
                            yield json.loads(line)

        return _stream()  # Returns async generator

    # Example of a synchronous utility to normalize raw responses
    def _normalize_response(self, raw: dict) -> dict:
        return {
            "choices": raw.get("choices", []),
            "usage": raw.get("usage", {}),
            "metadata": raw.get("metadata", {}),
        }


if __name__ == "__main__":
    client = HostedLLMClient()
    # Simple test call – will fail without proper env vars
    try:
        print(
            client.generate(
                {
                    "model": "gpt-4o-mini",
                    "messages": [{"role": "user", "content": "Hello"}],
                }
            )
        )
    except Exception as e:
        print("Test failed (expected without credentials):", e)
