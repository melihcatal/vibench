import os
import json
from vision_client import VisionClient


def describe_image(image_path: str) -> dict:
    """Generate a concise visual description for an image.

    Uses Alibaba Cloud Vision (Image Content) service as the concrete provider.
    The provider is identifiable by the import `alibabacloud_vision` and env vars.

    Args:
        image_path: Path to the local image file.

    Returns:
        Dict with keys:
            - 'description': short human-readable caption.
    """
    client = VisionClient()
    response = client.describe_image(image_path)
    # Normalize to our internal shape
    return {"description": response.get("description", "")}


if __name__ == "__main__":
    img = "example.jpg"
    print(json.dumps(describe_image(img), ensure_ascii=False, indent=2))
