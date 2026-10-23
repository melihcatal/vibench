from typing import Any, Dict


class LLMRequest:
    def __init__(
        self, prompt: str, max_output_tokens: int = 500, temperature: float = 0.7
    ):
        self.prompt = prompt
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature


class LLMResponse:
    def __init__(self, text: str, raw: Any):
        self.text = text
        self.raw = raw


def normalize_response(raw_response: Any) -> LLMResponse:
    """Converts raw API response to a uniform LLMResponse object."""
    if isinstance(raw_response, dict):
        # Some APIs return dict with a .candidates field
        text = raw_response.get("text", "").strip()
        if not text:
            # Fallback: join multiple generated candidates
            text = "\\n".join(
                [c.get("text", "").strip() for c in raw_response.get("candidates", [])]
            ).strip()
        return LLMResponse(text, raw_response)
    else:
        # Default fallback for simple text responses
        return LLMResponse(raw_response.strip(), raw_response)
