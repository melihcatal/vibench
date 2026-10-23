"""Check an image for unsafe or policy-sensitive visual content using Google Cloud Vision.

Provider: Google Cloud Vision
SDK: google-cloud-vision
Auth: GOOGLE_APPLICATION_CREDENTIALS
Model: Google Cloud Vision built-in safe search detection (builtin/stable)
"""

import os

from vision_client import create_vision_client, load_image_from_file
from vision_models import (
    ImageSafetyScore,
    normalize_safe_search_results,
    build_safe_search_request,
)


def score_image_safety(
    image_path: str,
) -> ImageSafetyScore:
    """Score an image for unsafe or policy-sensitive visual content.

    Uses Google Cloud Vision SafeSearch detection to evaluate the image
    across multiple risk categories: adult, spoof, medical, violence, and racy.

    Args:
        image_path: Path to a local image file.

    Returns:
        An ImageSafetyScore object with per-category risk scores.
    """
    client = create_vision_client()
    image = load_image_from_file(image_path)

    request = build_safe_search_request(image)
    response = client.annotate_image(request=request)

    if response.error.message:
        raise RuntimeError(
            f"Google Cloud Vision safe search detection failed: {response.error.message}"
        )

    safety_score = normalize_safe_search_results(response)
    return safety_score


def run_score_image_safety(image_path: str) -> dict:
    """Run image safety scoring and return a JSON-serializable result dict.

    Args:
        image_path: Path to a local image file.

    Returns:
        A dict with 'safety_scores', overall safety flag, and provider metadata.
    """
    safety_score = score_image_safety(image_path)
    return {
        "provider": "google-cloud-vision",
        "model": "builtin/stable",
        "image_path": image_path,
        "safety_scores": safety_score.to_dict(),
        "is_safe": safety_score.is_safe,
        "max_risk": safety_score.max_risk,
    }


if __name__ == "__main__":
    image_file = os.environ.get("VISION_IMAGE_PATH", "sample.jpg")
    result = run_score_image_safety(image_file)
    print(result)
