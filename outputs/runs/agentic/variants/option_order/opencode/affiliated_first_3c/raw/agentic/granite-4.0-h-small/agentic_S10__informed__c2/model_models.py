from typing import TypedDict, Dict, Any


class LLMRequest(TypedDict):
    """Normalized request structure for any hosted LLM inference call."""

    model_id: str
    system_prompt: str
    user_input: str
    max_new_tokens: int


class LLMResponse(TypedDict):
    """Normalized response structure containing generated text."""

    text: str


class NormalizedClient:
    """Abstract wrapper that any provider-specific client (e.g., IBM watsonx.ai) must implement."""

    def generate(self, system_prompt: str, user_input: str, max_new_tokens: int) -> str:
        """Generate text and return only the generated portion."""
        raise NotImplementedError()


def normalize_response(raw: Dict[str, Any]) -> LLMResponse:
    """Extract the raw generated text from provider-specific payload formats."""
    # Default assumes the key 'text' exists; adapt per provider if needed.
    return {"text": raw.get("text", "")}
