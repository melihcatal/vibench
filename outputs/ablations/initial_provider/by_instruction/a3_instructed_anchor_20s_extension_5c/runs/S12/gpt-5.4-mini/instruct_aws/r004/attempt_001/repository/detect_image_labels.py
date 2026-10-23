from typing import Any, Dict

from vision_client import load_image_input, rekognition_client
from vision_models import VisionResult, normalize_labels


def detect_image_labels(image_path: str, max_labels: int = 10, min_confidence: float = 50.0) -> VisionResult:
    image = load_image_input(image_path)
    client = rekognition_client()
    response = client.detect_labels(Image={"Bytes": image.image_bytes}, MaxLabels=max_labels, MinConfidence=min_confidence)
    labels = normalize_labels(
        [{"name": item.get("Name"), "confidence": float(item.get("Confidence", 0.0)), "parents": [p.get("Name") for p in item.get("Parents", [])]} for item in response.get("Labels", [])]
    )
    return VisionResult(provider="aws.rekognition", kind="labels", source=image.image_path, data={"labels": labels})


def main() -> None:
    import json
    import sys

    result = detect_image_labels(sys.argv[1])
    print(json.dumps(result.__dict__, ensure_ascii=False))


if __name__ == "__main__":
    main()
