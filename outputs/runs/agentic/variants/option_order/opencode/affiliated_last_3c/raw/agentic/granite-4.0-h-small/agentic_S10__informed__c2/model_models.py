from typing import Any, Dict

# Provider: DashScope Qwen API (placeholder for request/response helpers)


class LLMRequest:
    """Simple wrapper for a request payload to the hosted LLM."""

    def __init__(self, messages: list[dict[str, Any]], temperature: float = 0.7):
        self.messages = messages
        self.temperature = temperature


class LLMResponse:
    """Wrapper for the raw response from the hosted LLM."""

    def __init__(self, raw: Any):
        self.raw = raw

    @property
    def content(self) -> str:
        # Assuming the raw response follows the DashScope chat format
        return self.raw.choices[0].message.content


# Normalization helper—translate provider-specific response into a
# uniform LLMResponse object


def normalize_response(provider_response: Any) -> LLMResponse:
    return LLMResponse(provider_response)
