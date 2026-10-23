from __future__ import annotations

import typing as t

# Request / Response / Normalization helpers for Hosted LLM Inference


def create_chat_message(role: str, content: str) -> dict:
    """Normalize a message into a provider‑agnostic chat message shape."""
    return {"role": role, "content": content}


def normalize_chat_response(resp: str) -> dict:
    """Parse and normalize a chat completion response to a unified dict format."""
    # Many SDKs return a string; here we just wrap it as a single content block.
    return {"role": "assistant", "content": resp}


class LLMConfig:
    """Encapsulate common inference parameters."""

    model: str
    temperature: float = 0.2
    max_tokens: int = 512

    def to_kwargs(self) -> dict:
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }


# Example usage (not executed): #
# cfg = LLMConfig(model="gemini-1.5-flash")
# params = cfg.to_kwargs()
