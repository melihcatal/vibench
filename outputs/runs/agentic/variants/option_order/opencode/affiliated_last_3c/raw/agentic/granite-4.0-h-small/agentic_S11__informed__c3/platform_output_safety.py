import json
from model_models import NormalizedResponse


def check_platform_output_for_unsafe(content: str) -> bool:
    """Placeholder safety check – replace with real moderation API call."""
    # Example: return False if content contains disallowed terms
    unsafe_terms = ["hate", "violence", "sexual", "discrimination"]
    return any(term in content.lower() for term in unsafe_terms)


def safe_platform_output(response: NormalizedResponse) -> NormalizedResponse:
    """Filter or annotate platform model output for unsafe content."""
    if check_platform_output_for_unsafe(response["content"]):
        # Annotate the result as unsafe (client can decide how to handle)
        return {
            **response,
            "metadata": {**response.get("metadata", {}), "safety": "unsafe"},
        }
    return response
