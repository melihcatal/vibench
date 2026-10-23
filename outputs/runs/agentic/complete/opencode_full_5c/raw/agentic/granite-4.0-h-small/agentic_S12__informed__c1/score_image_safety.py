import os
import json
from vision_client import VisionClient


def score_image_safety(image_path: str) -> dict:
    """Check an image for unsafe or policy‑sensitive visual content.

    Provider: Alibaba Cloud Vision Content Moderation (Image Safety).
    Identifiable by the SDK import `alibabacloud_vision` and credentials from env vars.

    Args:
        image_path: Local path to the image file.

    Returns:
        Dict with keys:
            - 'is_safe': True when no violations detected, else False.
            - 'violations': list of detected issue names (e.g., 'violence', 'porn').
    """
    client = VisionClient()
    result = client.moderate_image(image_path)
    violations = result.get("labels", [])
    is_safe = not violations
    return {"is_safe": is_safe, "violations": violations}


if __name__ == "__main__":
    img = "example.jpg"
    print(json.dumps(score_image_safety(img), ensure_ascii=False, indent=2))
