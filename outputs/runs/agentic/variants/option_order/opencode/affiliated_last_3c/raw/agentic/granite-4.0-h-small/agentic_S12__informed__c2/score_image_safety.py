# score_image_safety.py
import json
from vision_client import VisionClient


def score_image_safety(image_path: str) -> dict:
    """Check an image for unsafe or policy‑sensitive visual content using a concrete provider.

    Uses Azure AI Content Safety SDK for demonstration.
    """
    client = VisionClient()
    safety_report = client.safety_check(image_path)
    # Normalize to a simple boolean flag + optional details
    is_safe = safety_report.get("safe", True)
    details = safety_report.get("details", [])
    return {"safe": is_safe, "details": details}
