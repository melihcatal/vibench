import os
import sys
from pathlib import Path

from google.cloud import vision


def extract_text(image_path: str) -> str:
    client = vision.ImageAnnotatorClient()
    content = Path(image_path).read_bytes()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise RuntimeError(response.error.message)
    return response.full_text_annotation.text or ""


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <image_path>", file=sys.stderr)
        return 2
    image_path = sys.argv[1]
    if not os.path.isfile(image_path):
        print(f"File not found: {image_path}", file=sys.stderr)
        return 1
    print(extract_text(image_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
