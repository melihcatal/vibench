from typing import Any, Dict, List

class ModelResource:
    """Encapsulates a provider-specific model/deployment handle."""
    def __init__(self, provider: str, model: str = None, deployment: str = None):
        self.provider = provider
        self.model = model
        self.deployment = deployment

    def __repr__(self) -> str:
        parts = []
        if self.provider:
            parts.append(f"provider={self.provider}")
        if self.model:
            parts.append(f"model={self.model}")
        if self.deployment:
            parts.append(f"deployment={self.deployment}")
        return "ModelResource(" + ", ".join(parts) + ")"


class NormalizedResponse:
    """Normalization layer for OpenAI chat completion output."""
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def from_openai(cls, raw: Dict[str, Any]) -> Any:
        """Convert raw OpenAI response into a structured response."""
        # Extract useful fields
        choices = raw.get("choices", [])
        if not choices:
            raise ValueError("No choices in response")
        first = choices[0]
        output = {
            "generated_text": first.get("message", {}).get("content", ""),
            "finish_reason": first.get("finish_reason"),
            "usage": raw.get("usage"),
            "model": raw.get("model"),
            "request_id": raw.get("id"),
        }
        return cls(data=output)

    def __repr__(self) -> str:
        return f"NormalizedResponse({self.data})"

# Optional: further helpers for payload transformation can be added here.
