import os
import json
from vision_client import VisionClient


def detect_image_labels(image_path: str) -> list:
    """Detect objects/labels in a static image using Alibaba Cloud Vision API.

    Returns a list of detected label strings.
    """
    client = VisionClient()
    # Load image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    # Call provider SDK (Alibaba Cloud Vision)
    response = client.detect_labels(image_bytes)
    # Normalize response to simple list of labels
    labels = [label["name"] for label in response.get("labels", [])]
    return labels


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Detect labels in a static image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()
    labels = detect_image_labels(args.image_path)
    print(json.dumps({"labels": labels}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
