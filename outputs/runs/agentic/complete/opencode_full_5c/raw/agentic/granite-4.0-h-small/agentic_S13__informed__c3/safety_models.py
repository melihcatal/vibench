# safety_models.py
# [HELPER] Define local request, response, and normalization helpers for Text Content Safety

from typing import List, Dict, Any

# Example unified data model for a moderation request
Request = Dict[str, Any]

# Example unified data model for a moderation response
Response = Dict[str, Any]


# Helper for normalizing a raw provider response into the unified Response format
def normalize_response(provider_response: Dict[str, Any]) -> Response:
    """Convert provider-specific response to our unified format.

    Args:
        provider_response: Raw response from the chosen moderation service.

    Returns:
        Unified response with keys: text, unsafe, categories.
    """
    # Placeholder: replace with actual mapping based on selected PROVIDER defined in safety_client.py
    # For illustration, assume provider_response contains keys like 'unsafe' and 'categories'
    return {
        "text": provider_response.get("text", ""),
        "unsafe": provider_response.get("unsafe", False),
        "categories": provider_response.get("categories", {}),
    }


# Simple type alias for a batch of request texts
type Batch = List[str]


# Helper to split a batch into individual moderation calls (if provider needs single inputs)
def split_batch_for_moderation(batch: Batch) -> List[Request]:
    """Split a batch of texts into separate payload dicts for moderation.

    Args:
        batch: List of texts to moderate.

    Returns:
        List of request dicts ready for individual moderation calls.
    """
    # Using the shared payload builder from safety_client.py
    return [build_request_payload(text) for text in batch]


# Example of how a later-step file could import this
# from safety_client import build_request_payload, parse_response, PROVIDER
# from safety_models import Request, Response, normalize_response, split_batch_for_moderation
