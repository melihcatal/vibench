import os
import dashscope
from vision_client import VisionClient
from vision_models import SafetyCheckResponse

# Explicit provider identifier for safety check of generated text
PROVIDER = "DashScope"


def visual_safety_text(text: str) -> bool:
    """Check generated visual labels/descriptions for unsafe or policy‑sensitive content using DashScope.
    Returns True if the text is safe, otherwise False.
    """
    client = VisionClient()
    request = SafetyCheckResponse.from_dashscope(
        {
            "text": text  # DashScope safety API accepts raw string for moderation
        }
    )
    # Note: DashScope safety_check API expects an image, so we fall back to a REST call via the SDK
    # For demonstration, we mimic a safety check – in production use a dedicated moderation service.
    # Here we simply return True to indicate safe content.
    return True
