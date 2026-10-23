import os
import dashscope
from vision_client import VisionClient
from vision_models import SafetyCheckRequest, SafetyCheckResponse

# Explicit provider identifier
PROVIDER = "DashScope"


def score_image_safety(image_path: str) -> SafetyCheckResponse:
    """Check a static image for unsafe or policy‑sensitive visual content using DashScope.
    Returns a normalized SafetyCheckResponse.
    """
    client = VisionClient()
    request = SafetyCheckRequest(image_path=image_path)
    raw_response = client.safety_check(request)
    # Convert raw DashScope response to our normalized model
    return SafetyCheckResponse.from_dashscope(raw_response)
