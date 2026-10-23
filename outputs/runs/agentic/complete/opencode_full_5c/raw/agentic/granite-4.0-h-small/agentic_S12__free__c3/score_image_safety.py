# score_image_safety.py
# [SAME-SCENARIO]

from vision_client import VisionClient
from vision_models import SafetyCheckResponse, normalize_safety_check

# Use Google Cloud SafeSearch as the concrete provider
# Google SafeSearch detects unsafe or policy-sensitive visual content


def check_safety(image_path: str) -> SafetyCheckResponse:
    """Check an image for unsafe or policy-sensitive visual content using Google SafeSearch.

    Returns a normalized SafetyCheckResponse indicating the safety status.
    """
    client = VisionClient()  # Google SafeSearch client configured internally
    raw_resp = client.safe_search_detection(image_path)
    return normalize_safety_check(raw_resp)
