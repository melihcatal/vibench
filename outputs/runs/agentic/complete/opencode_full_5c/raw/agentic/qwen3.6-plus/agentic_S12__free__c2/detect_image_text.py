import os
import base64
from typing import Optional, List
import boto3
from botocore.config import Config

from vision_client import get_rekognition_client, load_image_bytes
from vision_models import ImageTextRequest, ImageTextResponse, DetectedTextBlock


def detect_image_text(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    detect_orientation: bool = True,
) -> ImageTextResponse:
    if image_path is None and image_bytes is None:
        raise ValueError("Either image_path or image_bytes must be provided")

    if image_bytes is None:
        image_bytes = load_image_bytes(image_path)

    client = get_rekognition_client()

    payload: Dict = {
        "Image": {"Bytes": image_bytes},
    }

    response = client.detect_text(**payload)

    text_blocks = []
    for text_item in response.get("TextDetections", []):
        block = DetectedTextBlock(
            detected_text=text_item["DetectedText"],
            text_type=text_item["Type"],
            confidence=text_item["Confidence"],
            bounding_box=text_item.get("Geometry", {}).get("BoundingBox", {}),
            parent_id=text_item.get("ParentId"),
            id=text_item.get("Id"),
        )
        text_blocks.append(block)

    lines = [b for b in text_blocks if b.text_type == "LINE"]
    words = [b for b in text_blocks if b.text_type == "WORD"]

    full_text = " ".join(line.detected_text for line in lines)

    return ImageTextResponse(
        text_blocks=text_blocks,
        full_text=full_text,
        lines=lines,
        words=words,
        model="aws-rekognition-detect-text-v3",
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_image_text.py <image_path>")
        sys.exit(1)

    result = detect_image_text(image_path=sys.argv[1])
    print(f"Full text: {result.full_text}")
    print(f"Lines found: {len(result.lines)}")
    print(f"Words found: {len(result.words)}")
