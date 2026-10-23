import os
from vision_client import VisionClient


def score_image_safety(image_path: str) -> bool:
    """Check image for unsafe/policy-sensitive visual content using Google Cloud Content Safety.

    Args:
        image_path: Path to the input image file.

    Returns:
        True if safe, False if unsafe or flagged.
    """
    client = VisionClient(service="google-cloud-vision")
    # Approximate safety check via annotation types (replace with actual safety API as needed)
    response = client.annotate_image(image_path, features=["SAFE_SEARCH_DETECTION"])
    safe = response.get("safeSearchAnnotation", {})
    # Simple heuristic: if adult or violent flags are HIGH, consider unsafe
    unsafe = (
        safe.get("adult", "NONE") == "HIGH" or safe.get("violent", "NONE") == "HIGH"
    )
    return not unsafe
