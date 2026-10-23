import os
import json
from vision_client import VisionClient


def score_image_safety(image_path: str) -> bool:
    """Check an image for unsafe or policy-sensitive visual content.

    Returns True if safe, False if unsafe.
    """
    client = VisionClient()
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    response = client.check_safety(image_bytes)
    # Assume response contains a boolean "safe" flag
    safe = response.get("safe", False)
    return safe


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Assess safety of an image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()
    is_safe = score_image_safety(args.image_path)
    print(json.dumps({"safe": is_safe}, indent=2))
