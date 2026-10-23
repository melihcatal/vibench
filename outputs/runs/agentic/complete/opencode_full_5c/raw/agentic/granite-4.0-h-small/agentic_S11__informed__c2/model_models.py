# [HELPER] model_models.py

# Local request, response, and normalization helpers for Managed Model Platform Workflow
from typing import Any, Dict


# ----------- Request schema -----------
class ModelRequest:
    def __init__(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7):
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.temperature = temperature

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }


# ----------- Response normalization -----------
class ModelResponse:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw

    @property
    def content(self) -> str:
        # Normalizes different provider payload structures to a common field
        if isinstance(self.raw, dict):
            # Example for Bedrock (list of generations)
            if self.raw.get("outputs"):
                return self.raw["outputs"][0].get("content", "")
            # Example for Hugging Face (single string)
            return self.raw.get("generated_text", "")
        return ""

    @property
    def usage(self) -> Dict[str, int]:
        # Common usage keys: input_tokens, output_tokens
        if isinstance(self.raw, dict):
            meta = self.raw.get("metadata", {})
            return {
                "input_tokens": meta.get("inputTokenCount", 0),
                "output_tokens": meta.get("outputTokenCount", 0),
            }
        return {}

    @property
    def request_id(self) -> str:
        return self.raw.get("requestId", "")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "usage": self.usage,
            "request_id": self.request_id,
        }
