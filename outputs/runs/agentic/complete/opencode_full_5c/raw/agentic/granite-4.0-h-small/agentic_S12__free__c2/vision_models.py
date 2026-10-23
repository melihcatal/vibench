from typing import TypedDict, Literal

# Type definitions for consistent request/response shapes across files


class VisionRequest(TypedDict):
    model: str
    prompt: str
    image: Dict[str, str]
    # Additional provider‑specific fields can be added here


class VisionTypedResponse(TypedDict):
    labels: list[str]
    description: str
    text: list[str]
    safe: bool
    # Extend as needed for other capabilities


# Optional alias for provider‑agnostic response schema
VisionResponse = VisionTypedResponse

# Export for local helpers and later‑step files
__all__ = ["VisionRequest", "VisionResponse"]
