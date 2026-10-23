# Request, response, and normalization helpers for hosted LLM inference
import json
import typing as t


class LLMRequest:
    """Encapsulate request payload for hosted LLM calls."""

    def __init__(
        self, model: str, messages: t.List[t.Dict[str, str]], temperature: float = 0.2
    ):
        self.model = model
        self.messages = messages
        self.temperature = temperature

    def to_dict(self) -> dict:
        """Convert to provider-specific payload format."""
        return {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
        }


class LLMResponse:
    """Encapsulate raw response from hosted LLM providers."""

    def __init__(self, raw: dict):
        self.raw = raw
        self.choices = raw.get("choices", [])

    def get_content(self) -> t.Optional[str]:
        """Extract the textual content from the response."""
        if not self.choices:
            return None
        # Default assumption: OpenAI-like format
        return self.choices[0].get("message", {}).get("content", "")

    def parse_json(self) -> t.Optional[t.Any]:
        """Attempt to parse response as JSON."""
        content = self.get_content()
        if not content:
            return None
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return None


def normalize_response(raw: dict) -> LLMResponse:
    """Normalize different provider responses to a common wrapper."""
    return LLMResponse(raw)
