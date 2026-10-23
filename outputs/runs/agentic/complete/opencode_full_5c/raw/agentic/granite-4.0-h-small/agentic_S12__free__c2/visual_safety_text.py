from vision_client import parse_vision_response
from vision_models import VisionResponse


# Check generated textual labels for unsafe/policy violations
def visual_safety_text(raw_labels: List[str]) -> bool:
    """Run a safety scan on detected labels or extracted text.","""
    # Placeholder for a concrete safety provider (e.g., OpenAI Moderation API)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    # Example: batch check each label
    unsafe = any(label.lower() in ["adult", "violence", "hate"] for label in raw_labels)
    return not unsafe


# Export for later step pipelines
__all__ = ["visual_safety_text"]
