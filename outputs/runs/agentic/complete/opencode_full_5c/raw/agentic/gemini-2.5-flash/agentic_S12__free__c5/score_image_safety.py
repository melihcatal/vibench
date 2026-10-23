import os
from vision_client import get_vision_client
from vision_models import (
    create_image_from_bytes,
    load_image_from_file,
    get_safe_search_results,
)
from google.cloud.vision_v1 import Feature


def score_image_safety(image_path: str) -> dict:
    client = get_vision_client()
    image_bytes = load_image_from_file(image_path)
    image = create_image_from_bytes(image_bytes)

    features = [Feature(type_=Feature.Type.SAFE_SEARCH_DETECTION)]
    response = client.annotate_image(
        {
            "image": image,
            "features": features,
        }
    )

    return get_safe_search_results(response)


if __name__ == "__main__":
    # Example usage: Replace with your image path
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    dummy_image_path = "test_image.jpg"
    if not os.path.exists(dummy_image_path):
        # In a real scenario, you'd have an actual image.
        # Here we're just creating a placeholder.
        with open(dummy_image_path, "w") as f:
            f.write(
                "dummy image content"
            )  # This won't work for actual vision API, but allows the script to run without erroring on file not found.

    safety_scores = score_image_safety(dummy_image_path)
    print(f"Image safety scores: {safety_scores}")
