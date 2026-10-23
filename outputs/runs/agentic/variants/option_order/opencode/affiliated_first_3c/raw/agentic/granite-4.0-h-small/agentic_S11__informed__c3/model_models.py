# model_models.py
# [HELPER] Define local request, response, and normalization helpers for Managed Model Platform Workflow

# Provider: IBM watsonx.ai (used throughout the same-scenario helpers)
import json
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass

class GenerationRequest:
    """Normalized request payload for generative model calls."""
    deployment_id: str
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 512

    def to_watsonx(self) -> Dict[str, Any]:
        """Convert to watsonx.ai payload format."""
        return {
            "deployment_id": self.deployment_id,
            "prompt": self.prompt,
            "parameters": {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
        }

@dataclass

class GenerationResponse:
    """Normalized response model, hiding provider specifics."""
    output: str
    metadata: Dict[str, Any]

    @staticmethod
def from_raw(raw: Dict[str, Any]) -> Any:
        """Create a normalized response from watsonx.ai raw response."""
        return GenerationResponse(
            output=raw.get("text", ""),
            metadata=raw.get("usage")  # could be richer depending on provider
        )

# Helper to standardize output across providers

def normalize_response(raw: Dict[str, Any]) -> GenerationResponse:
    """Transform a provider-specific raw payload into the unified model response."""
    # For watsonx.ai the raw dict looks like: {"text": ..., "usage": {...}, "request_id": ...}
    return GenerationResponse(
        output=raw.get("text", ""),
        metadata=raw.get("usage")
    )

# Example usage (standalone)
if __name__ == "__main__":
    raw = {
        "text": "Hello world!",
        "usage": {"prompt_tokens": 5, "total_tokens": 5},
        "request_id": "abc123"
    }
    norm = normalize_response(raw)
    print(asdict(norm))