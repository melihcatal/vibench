import os
from google.cloud import vision
from vision_client import get_vision_client


def detect_image_labels(image_path: str, max_results: int = 10):
    """Detects labels or objects in a static image using Google Cloud Vision API."""
    client = get_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image, max_results=max_results)
    labels = response.label_annotations

    result = []
    for label in labels:
        result.append(
            {
                "description": label.description,
                "score": label.score,
                "topicality": label.topicality,
                "mid": label.mid,
            }
        )

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python detect_image_labels.py <image_path>")
        sys.exit(1)

    labels = detect_image_labels(sys.argv[1])
    for label in labels:
        print(f"{label['description']}: {label['score']:.2f}")
