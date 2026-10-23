from __future__ import annotations

from google.cloud import vision

from vision_client import build_client, make_image
from vision_models import ImageAnalysisRequest, normalize_labels


def detect_image_labels(image_path: str, max_results: int = 10):
    request = ImageAnalysisRequest(image_path=image_path, max_results=max_results)
    client = build_client()
    image = make_image(request.image_path)
    response = client.label_detection(image=image, max_results=request.max_results)
    return normalize_labels(response.label_annotations)


def main(image_path: str) -> None:
    labels = detect_image_labels(image_path)
    for label in labels:
        print(f"{label.name}\t{label.score:.3f}")


if __name__ == "__main__":
    raise SystemExit("Use detect_image_labels(image_path) from your application code.")
