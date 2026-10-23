from typing import Any, NamedTuple

class RequestPayload(NamedTuple):
    """Represents a simple request to the model platform."""
    prompt: str

class ResponseWithMetadata(NamedTuple):
    """
    Represents a model response that includes provider-specific metadata.
    """
    text: str
    provider_response: Any

