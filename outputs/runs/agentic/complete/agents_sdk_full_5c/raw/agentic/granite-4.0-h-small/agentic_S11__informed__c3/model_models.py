# model_models.py
# Local helper: Request, response, and normalization models for Managed Model Platform Workflow

from typing import TypedDict, List, Any

# ---------------------------------------------------------------------------
# Input data structures
# ---------------------------------------------------------------------------
class UserMessage(TypedDict):
    role: str  # e.g., \"user\", \"assistant\"
    content: str

class SystemMessage(TypedDict):
    role: str
    content: str

class ChatRequest(TypedDict):
    messages: List[UserMessage | SystemMessage]
    model: str  # Vertex AI model family or ID
    temperature: float = 0.7
    # Additional provider-specific fields can be added here

# ---------------------------------------------------------------------------
# Normalized response structures (common across providers)
# ---------------------------------------------------------------------------
class NormalizedResponse(TypedDict):
    model: str
    usage: dict  # provider usage breakdown (tokens, etc.)
    content: List[str]  # text chunks produced by the model
    metadata: dict  # optional platform metadata

# ---------------------------------------------------------------------------
# Example normalization helper
# ---------------------------------------------------------------------------

def normalize_vertex_response(raw: Any) -> NormalizedResponse:
    """
    Convert a raw Vertex AI response to a provider-agnostic format.

    Args:
        raw (Any): Raw response object returned by genai.GenerativeModel.generate_content.

    Returns:
        NormalizedResponse: Structured output useful for downstream steps.
    """
    # Vertex AI responses expose a .text attribute and .request.metadata for usage.
    usage_info = getattr(raw.request.metadata, 'usageInfo', {})  # dict-like
    return NormalizedResponse(
        model=raw.model,
        usage=usage_info,
        content=[raw.text],
        metadata={"requestId": getattr(raw.request.metadata, 'requestId', None)}
    )

# Example usage (uncomment to test)
#if __name__ == "__main__":
#    from model_client import configure_client, get_generative_model
#    configure_client()
#    model = get_generative_model("gemini-1.5-flash")
#    raw_resp = model.generate_content("Explain quantum computing in simple terms.")
#    print(normalize_vertex_response(raw_resp))
