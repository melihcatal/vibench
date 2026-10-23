import os
import base64
from typing import Optional, List
import boto3
from botocore.config import Config

from vision_client import get_rekognition_client, load_image_bytes
from vision_models import ImageDescriptionRequest, ImageDescriptionResponse


def describe_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    max_descriptions: int = 3,
    min_confidence: float = 60.0,
) -> ImageDescriptionResponse:
    if image_path is None and image_bytes is None:
        raise ValueError("Either image_path or image_bytes must be provided")

    if image_bytes is None:
        image_bytes = load_image_bytes(image_path)

    client = get_rekognition_client()

    label_response = client.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=20,
        MinConfidence=min_confidence,
    )

    scene_response = client.detect_labels(
        Image={"Bytes": image_bytes},
        MaxLabels=10,
        MinConfidence=min_confidence,
    )

    labels = label_response.get("Labels", [])
    scene_labels = [
        lbl
        for lbl in scene_response.get("Labels", [])
        if any(
            p["Name"].lower()
            in ("scene", "environment", "landscape", "indoor", "outdoor")
            for p in lbl.get("Parents", [])
        )
    ]

    descriptions = _build_descriptions(labels, scene_labels, max_descriptions)

    return ImageDescriptionResponse(
        descriptions=descriptions,
        model="aws-rekognition-describe-image-v3",
        primary_labels=[lbl["Name"] for lbl in labels[:5]],
    )


def _build_descriptions(
    labels: List[dict],
    scene_labels: List[dict],
    max_descriptions: int,
) -> List[str]:
    descriptions = []

    if scene_labels:
        top_scene = scene_labels[0]
        descriptions.append(
            f"The image shows a {top_scene['Name'].lower()} scene "
            f"with {top_scene['Confidence']:.0f}% confidence."
        )

    objects = [lbl for lbl in labels if not lbl.get("Instances")]
    if objects:
        top_objects = objects[:3]
        object_names = ", ".join(o["Name"].lower() for o in top_objects)
        descriptions.append(f"Key objects detected: {object_names}.")

    instances = [lbl for lbl in labels if lbl.get("Instances")]
    if instances:
        inst = instances[0]
        descriptions.append(
            f"Detected {len(inst['Instances'])} instance(s) of {inst['Name'].lower()}."
        )

    return descriptions[:max_descriptions]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python describe_image.py <image_path>")
        sys.exit(1)

    result = describe_image(image_path=sys.argv[1])
    for desc in result.descriptions:
        print(desc)
