from typing import Optional
from vision_client import (
    prepare_image_bytes,
    get_rekognition_client,
    call_rekognition_detect_labels,
)
from vision_models import ImageDescriptionResponse, parse_rekognition_labels


def describe_image(
    image_url: Optional[str] = None,
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> ImageDescriptionResponse:
    image_data = prepare_image_bytes(
        image_url=image_url, image_path=image_path, image_bytes=image_bytes
    )
    client = get_rekognition_client()
    raw_response = call_rekognition_detect_labels(client, image_data)
    label_result = parse_rekognition_labels(raw_response, image_url=image_url)
    top_labels = sorted(label_result.labels, key=lambda l: l.confidence, reverse=True)[
        :10
    ]
    label_parts = [f"{lbl.name} ({lbl.confidence:.0f}%)" for lbl in top_labels]
    description = "The image contains: " + ", ".join(label_parts) + "."
    avg_confidence = (
        sum(lbl.confidence for lbl in top_labels) / len(top_labels)
        if top_labels
        else 0.0
    )
    return ImageDescriptionResponse(
        image_url=image_url,
        description=description,
        confidence=avg_confidence,
        raw_response=raw_response,
    )


if __name__ == "__main__":
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else None
    if source and source.startswith("http"):
        result = describe_image(image_url=source)
    elif source:
        result = describe_image(image_path=source)
    else:
        result = describe_image(image_url="https://example.com/sample.jpg")
    print(result.description)
