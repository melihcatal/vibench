import os
from vision_client import get_vision_client
from vision_models import (
    create_image_from_bytes,
    load_image_from_file,
    get_label_detection_results,
)
from google.cloud.vision_v1 import Feature


def detect_image_labels(image_path: str) -> list[str]:
    client = get_vision_client()
    image_bytes = load_image_from_file(image_path)
    image = create_image_from_bytes(image_bytes)

    features = [Feature(type_=Feature.Type.LABEL_DETECTION)]
    response = client.annotate_image(
        {
            "image": image,
            "features": features,
        }
    )

    return get_label_detection_results(response)


if __name__ == "__main__":
    # Example usage: Replace with your image path
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise for Google Cloud Vision API.
    # For local testing, you might need a dummy image file.
    # Create a dummy image file for testing if it doesn't exist
    dummy_image_path = "test_image.jpg"
    if not os.path.exists(dummy_image_path):
        # In a real scenario, you'd have an actual image.
        # Here we're just creating a placeholder.
        with open(dummy_image_path, "w") as f:
            f.write(
                "dummy image content"
            )  # This won't work for actual vision API, but allows the script to run without erroring on file not found.

    labels = detect_image_labels(dummy_image_path)
    print(f"Detected labels: {labels}")
