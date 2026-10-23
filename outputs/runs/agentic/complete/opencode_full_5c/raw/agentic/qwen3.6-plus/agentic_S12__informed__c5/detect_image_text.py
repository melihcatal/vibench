from typing import Optional
from vision_client import (
    prepare_image_bytes,
    get_rekognition_client,
    call_rekognition_detect_text,
)
from vision_models import TextDetectionResponse, parse_rekognition_text


def detect_image_text(
    image_url: Optional[str] = None,
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> TextDetectionResponse:
    image_data = prepare_image_bytes(
        image_url=image_url, image_path=image_path, image_bytes=image_bytes
    )
    client = get_rekognition_client()
    raw_response = call_rekognition_detect_text(client, image_data)
    result = parse_rekognition_text(raw_response, image_url=image_url)
    return result


if __name__ == "__main__":
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else None
    if source and source.startswith("http"):
        result = detect_image_text(image_url=source)
    elif source:
        result = detect_image_text(image_path=source)
    else:
        result = detect_image_text(image_url="https://example.com/sample.jpg")
    print(result.full_text)
    for txt in result.detected_text:
        if txt.type_ == "WORD":
            print(f"  WORD: {txt.text} ({txt.confidence:.1f}%)")
