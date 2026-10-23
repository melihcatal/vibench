from typing import TypedDict, List, Dict, Any

# Request schema for a hosted LLM inference call
# Each concrete provider may have its own exact payload shape.
class LLMRequest(TypedDict):
    model: str  # Identifier for the hosted model family
text: str   # Prompt or input text
    max_tokens: int = 256
    temperature: float = 0.7

# Normalized response from the LLM
# Normalization aims to provide a consistent structure across providers.
class LLMResponse(TypedDict):
    text: str
    usage: Dict[str, int]   # e.g., {"prompt_tokens": 12, "completion_tokens": 23}

class NormalizedResult(TypedDict):
    provider: str  # provider identifier (e.g., "openai")
    original_request: LLMRequest
    normalized_response: LLMResponse
    raw_response: Dict[str, Any]  # raw data returned by provider SDK/API

# Helper to normalize a raw provider response into the consistent format
def normalize_response(provider: str, raw: Dict[str, Any]) -> LLMResponse:
    if provider == "openai":
        # OpenAI returns choices[0].text and usage fields
        return {
            "text": raw.get("choices", [{}])[0].get("text", ""),
            "usage": raw.get("usage", {}),
        }
    # Add other providers here as needed
    raise NotImplementedError(f"Normalization for provider {provider} not implemented")
