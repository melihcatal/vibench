from typing import Any

from vision_client import as_image_payload, rekognition_client


def describe_image(image: Any) -> str:
    client = rekognition_client()
    response = client.detect_labels(
        Image=as_image_payload(image), MaxLabels=5, MinConfidence=80
    )
    labels = [
        item.get("Name", "")
        for item in response.get("Labels", [])[:3]
        if item.get("Name")
    ]
    return ", ".join(labels) if labels else "An image with visual content."
