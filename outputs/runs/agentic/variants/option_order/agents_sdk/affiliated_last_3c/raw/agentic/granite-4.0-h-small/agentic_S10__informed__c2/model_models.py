from typing import TypedDict, Any

# Request shape that can be expanded per provider
class LLMRequest(TypedDict):
    model: str
    messages: list[dict[str, str]]
    temperature: float
    # Provider‑specific extra fields can be added under **kwargs
    **kwargs: Any

# Normalized response shape returned to callers
class NormalizedLLMResponse(TypedDict):
    content: str
    # Optional fields for downstream processing
    usage: dict[str, int] = None
    token_count: int = None
    # Provider‑specific nested payload can be stored under raw
    raw: Any = None

# Normalization helpers

def normalize_response(provider_response: Any) -> NormalizedLLMResponse:
    """Convert provider‑specific raw response into a common shape."""
    # Example for DashScope Qwen (TypedDict fields are filled where possible)
    try:
        raw = provider_response.choices[0].message
        return NormalizedLLMResponse(
            content=raw.content if hasattr(raw, "content") else "",
            usage=getattr(provider_response, "usage", None),
            token_count=getattr(raw, "token_count", None),
            raw=provider_response
        )
    except Exception:
        # Fallback for other providers that use different path
        return NormalizedLLMResponse(content=str(provider_response))


def normalize_escaping(text: str) -> str:
    """Simple escaping for downstream pipelines (e.g., JSON safety)."""
    return text.replace('"', '\\"').replace('\n', ' ')  # minimal handling
