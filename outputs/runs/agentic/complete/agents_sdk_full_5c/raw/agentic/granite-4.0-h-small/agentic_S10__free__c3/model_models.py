from typing import Any, Dict, List, Optional

class InferenceResponse(Dict[str, Any]):
    """Normalized response container for LLM inference calls.

    Attributes:
        choices: List of choices returned by the provider (usually containing 'message').
        usage: Optional dict with token usage info.
    """
    def __init__(self, raw: Dict[str, Any]):
        super().__init__(raw)
        self.choices: List[Any] = raw.get("choices", [])
        self.usage: Optional[Dict[str, int]] = raw.get("usage")


def normalize_response(raw_response: Dict[str, Any]) -> InferenceResponse:
    """Convert a provider's raw JSON response into the common InferenceResponse.

    Args:
        raw_response: The dict returned by the concrete LLM client.

    Returns:
        A standardized InferenceResponse object.
    """
    # Simple normalization; adapt to each provider's schema as needed.
    return InferenceResponse(raw_response)
