from __future__ import annotations
from typing import TypedDict

# Common request/response shape for our hosted LLM inference helpers
# Not provider-specific, just a normalization layer used by downstream files


class ChatMessage(TypedDict):
    role: str  # 'system' | 'user' | 'assistant'
    content: str


class LLMRequest(TypedDict):
    model: str  # Model identifier (e.g., 'qwen')
    messages: list[ChatMessage]
    # Optional provider-specific overrides (ignored by generic client)
    temperature: float | None = None
    stream: bool = False


class LLMResponse(TypedDict):
    choices: list[dict[str, Any]]  # Raw response from the provider SDK


# Normalized view of the answer text
# Additional fields can be added for specific providers if needed


class NormalizedAnswer(TypedDict):
    text: str  # The generated text
    finish_reason: str | None = None  # May be 'length', 'stop', etc.


# Utility to normalize raw SDK response to our canonical format
def normalize_response(raw_response: dict) -> NormalizedAnswer:
    # Example normalization for DashScope output; add more as needed
    choice = raw_response.get("choices", [{}])[0]
    content = choice.get("message", {}).get("content", "")
    finish_reason = choice.get("finish_reason")
    return NormalizedAnswer(text=content, finish_reason=finish_reason)


# Example normalization for OpenAI SDK response (commented out)
# def normalize_openai_response(raw: dict) -> NormalizedAnswer:
#     choice = raw.get('choices', [{}])[0]
#     return NormalizedAnswer(text=choice['message']['content'], finish_reason=choice.get('finish_reason'))

# Example normalization for Anthropic SDK response (commented out)
# def normalize_anthropic_response(raw: dict) -> NormalizedAnswer:
#     choice = raw.get('choices', [{}])[0]
#     return NormalizedAnswer(text=choice['message']['content'], finish_reason=choice.get('finish_reason'))
