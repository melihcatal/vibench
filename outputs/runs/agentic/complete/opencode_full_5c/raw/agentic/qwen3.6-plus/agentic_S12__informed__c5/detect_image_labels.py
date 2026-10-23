from typing import Optional
from vision_client import (
    prepare_image_bytes,
    get_rekognition_client,
    call_rekognition_detect_labels,
)
from vision_models import LabelDetectionResponse, parse_rekognition_labels


def detect_image_labels(
    image_url: Optional[str] = None,
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> LabelDetectionResponse:
    image_data = prepare_image_bytes(
        image_url=image_url, image_path=image_path, image_bytes=image_bytes
    )
    client = get_rekognition_client()
    raw_response = call_rekognition_detect_labels(client, image_data)
    result = parse_rekognition_labels(raw_response, image_url=image_url)
    return result


if __name__ == "__main__":
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else None
    if source and source.startswith("http"):
        result = detect_image_labels(image_url=source)
    elif source:
        result = detect_image_labels(image_path=source)
    else:
        result = detect_image_labels(image_url="https://example.com/sample.jpg")
    for label in result.labels:
        print(f"{label.name}: {label.confidence:.1f}%")
