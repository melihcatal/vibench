"""Generate a short visual description for an image using Google Cloud Vision.

Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model: Google Cloud Vision built-in web detection (builtin/stable)
"""

import os

from vision_client import create_vision_client, load_image_from_file
from vision_models import (
    ImageDescription,
    normalize_web_description_results,
    build_image_description_request,
)


def describe_image(
    image_path: str,
) -> ImageDescription:
    """Generate a short visual description for a static image.

    Uses Google Cloud Vision Web Detection to extract best-guess labels
    and web entity descriptions that characterize the image content.

    Args:
        image_path: Path to a local image file.

    Returns:
        An ImageDescription object with text, confidence, and associated labels.
    """
    client = create_vision_client()
    image = load_image_from_file(image_path)

    request = build_image_description_request(image)
    response = client.annotate_image(request=request)

    if response.error.message:
        raise RuntimeError(
            f"Google Cloud Vision web detection failed: {response.error.message}"
        )

    description = normalize_web_description_results(response)
    return description


def run_describe_image(image_path: str) -> dict:
    """Run image description and return a JSON-serializable result dict.

    Args:
        image_path: Path to a local image file.

    Returns:
        A dict with 'description' and 'provider' metadata.
    """
    description = describe_image(image_path)
    return {
        "provider": "google-cloud-vision",
        "model": "builtin/stable",
        "image_path": image_path,
        "description": description.to_dict(),
    }


if __name__ == "__main__":
    image_file = os.environ.get("VISION_IMAGE_PATH", "sample.jpg")
    result = run_describe_image(image_file)
    print(result)
