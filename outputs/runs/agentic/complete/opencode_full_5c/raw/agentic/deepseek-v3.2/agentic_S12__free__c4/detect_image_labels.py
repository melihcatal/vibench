import os
from google.cloud import vision


def detect_image_labels(image_path):
    """
    Detects labels or objects in a static image using Google Cloud Vision API.

    Args:
        image_path: Path to the image file

    Returns:
        List of label annotations with descriptions and confidence scores
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if response.error.message:
        raise Exception(f"Google Cloud Vision API error: {response.error.message}")

    results = []
    for label in labels:
        results.append(
            {
                "description": label.description,
                "score": label.score,
                "mid": label.mid,
                "topicality": label.topicality,
            }
        )

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python detect_image_labels.py <image_path>")
        sys.exit(1)

    try:
        labels = detect_image_labels(sys.argv[1])
        for label in labels:
            print(f"{label['description']}: {label['score']:.2f}")
    except Exception as e:
        print(f"Error: {e}")
