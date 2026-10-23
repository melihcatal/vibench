import os
import json
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generate a short visual description of an image using Alibaba Cloud Vision API.

    Returns a concise one‑sentence description.
    """
    client = VisionClient()
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    response = client.describe_image(image_bytes)
    # Assume response contains a "description" field
    description = response.get("description", "No description found.")
    return description


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a short description for an image"
    )
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()
    print(describe_image(args.image_path))
