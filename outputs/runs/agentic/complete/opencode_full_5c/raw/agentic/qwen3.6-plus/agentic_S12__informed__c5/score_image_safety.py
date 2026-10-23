from typing import Optional
from vision_client import (
    prepare_image_bytes,
    get_rekognition_client,
    call_rekognition_detect_moderation,
)
from vision_models import SafetyScoreResponse, parse_rekognition_moderation


def score_image_safety(
    image_url: Optional[str] = None,
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    threshold: float = 50.0,
) -> SafetyScoreResponse:
    image_data = prepare_image_bytes(
        image_url=image_url, image_path=image_path, image_bytes=image_bytes
    )
    client = get_rekognition_client()
    raw_response = call_rekognition_detect_moderation(client, image_data)
    result = parse_rekognition_moderation(
        raw_response, image_url=image_url, threshold=threshold
    )
    return result


if __name__ == "__main__":
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else None
    if source and source.startswith("http"):
        result = score_image_safety(image_url=source)
    elif source:
        result = score_image_safety(image_path=source)
    else:
        result = score_image_safety(image_url="https://example.com/sample.jpg")
    print(f"Safe: {result.is_safe}")
    for label in result.moderation_labels:
        print(f"  {label.name}: {label.confidence:.1f}%")
