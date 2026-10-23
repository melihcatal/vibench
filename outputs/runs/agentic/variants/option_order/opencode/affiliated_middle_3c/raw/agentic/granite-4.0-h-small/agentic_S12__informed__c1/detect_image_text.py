import os
import json
from vision_client import VisionClient


def detect_image_text(image_path: str) -> list:
    """Extract text appearing inside an image using Alibaba Cloud Vision API.

    Returns a list of detected text blocks (strings).
    """
    client = VisionClient()
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    response = client.detect_text(image_bytes)
    # Normalize to list of strings
    texts = [text["content"] for text in response.get("texts", [])]
    return texts


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract text from an image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()
    texts = detect_image_text(args.image_path)
    print(json.dumps({"texts": texts}, ensure_ascii=False, indent=2))
