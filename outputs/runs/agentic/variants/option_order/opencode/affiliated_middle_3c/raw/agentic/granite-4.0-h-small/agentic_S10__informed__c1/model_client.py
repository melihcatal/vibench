import os
from typing import Dict, Any

# Local configuration helper – makes it easy to switch providers
# Provider identifiers are embedded in variables to keep code identifiable


class ModelClient:
    """Small wrapper around hosted LLM inference APIs.

    By default this client uses DashScope Qwen, but you can swap providers
    by changing the env vars below.  All auth values should be set in the
    runtime environment, never hard‑coded.
    """

    # ---------- Provider selection via environment ----------
    SERVICE = os.getenv("LLM_PROVIDER", "dashscope")  # default provider

    if SERVICE == "dashscope":
        API_KEY = os.getenv("DASHSCOPE_API_KEY")
        if not API_KEY:
            raise RuntimeError("Set DASHSCOPE_API_KEY env var for DashScope")
        # DashScope uses a simple SDK; model ID is fixed per use‑case
        MODEL_ID = "qwen"

    elif SERVICE == "anthropic":
        API_KEY = os.getenv("ANTHROPIC_API_KEY")
        if not API_KEY:
            raise RuntimeError("Set ANTHROPIC_API_KEY env var for Anthropic")
        MODEL_ID = "claude-3-5-sonnet-20240620"

    elif SERVICE == "mistral":
        API_KEY = os.getenv("MISTRAL_API_KEY")
        if not API_KEY:
            raise RuntimeError("Set MISTRAL_API_KEY env var for Mistral")
        MODEL_ID = "mistral-large-latest"

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {SERVICE}")

    # ---------- Generic request / response helpers ----------
    @staticmethod
    def _standardize_prompt(messages: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
        """Normalizes a list of message dicts to a common shape used by the SDK."""
        # DashScope, Anthropic, and Mistral all accept the same shape:
        # [{"role": ..., "content": ...}, ...]
        return messages

    @staticmethod
    def _extract_reply(response: Any) -> str:
        """Pulls the generated text out of a provider‑specific response."""
        # DashScope returns .choices[0].message.content
        # Anthropic returns .choices[0].message.content
        # Mistral returns .choices[0].message.content as well
        return response.choices[0].message.content

    # ---------- Public inference API ----------
    def summarize_text(self, text: str, max_tokens: int = 150) -> str:
        """Summarize arbitrary text using the selected provider."""
        messages = self._standardize_prompt([{"role": "user", "content": text}])
        # Dispatch based on provider
        if self.SERVICE == "dashscope":
            # DashScope chat completions (uses the same SDK method for all models)
            response = dashscope.chat.completions.create(
                model=self.MODEL_ID,
                messages=messages,
                max_tokens=max_tokens,
            )
        elif self.SERVICE == "anthropic":
            from anthropic import Anthropic, AnthropicClient

            client = Anthropic(api_key=self.API_KEY)
            response = client.completions.create(
                model=self.MODEL_ID,
                max_tokens=max_tokens,
                messages=messages,
            )
        elif self.SERVICE == "mistral":
            import mistralai

            client = mistralai.ChatClient(api_key=self.API_KEY)
            response = client.chat(
                model=self.MODEL_ID, messages=messages, max_tokens=max_tokens
            )
        else:
            raise NotImplementedError(
                f"Summarization not implemented for {self.SERVICE}"
            )
        return self._extract_reply(response)

    def extract_json(self, text: str, model: str = "qwen") -> dict:
        """Extract structured JSON from text using the selected provider."""
        messages = self._standardize_prompt([{"role": "user", "content": text}])
        if self.SERVICE == "dashscope":
            response = dashscope.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=200,
                temperature=0.0,
            )
        else:
            raise NotImplementedError(
                f"JSON extraction not implemented for {self.SERVICE}"
            )
        import json

        return json.loads(self._extract_reply(response))

    # Additional methods (answer_with_context, stream_completion, etc.)
    # can be added following the same pattern.
