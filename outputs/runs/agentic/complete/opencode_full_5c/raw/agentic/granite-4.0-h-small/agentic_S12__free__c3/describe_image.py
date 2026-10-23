# describe_image.py
# [SAME-SCENARIO]

from vision_client import VisionClient
from vision_models import CaptionResponse, normalize_caption

# Use Google Cloud Vision as the concrete provider
# Google Cloud Vision generates short descriptions (captions) for images


def generate_caption(image_path: str) -> CaptionResponse:
    """Generate a short visual description using Google Cloud Vision.

    Returns a normalized CaptionResponse containing the generated caption.
    """
    client = VisionClient()  # Google Vision client configured internally
    raw_resp = client.annotate_image(
        {
            "image": {"source": {"imageUri": f"gs://my-bucket/{image_path}"}},
            "features": [{"type_": "IMAGE_PROPERTIES"}],
        }
    )
    # Extract simple description from the response (placeholder logic)
    description = (
        raw_resp.get("responses", [{}])[0].get("fullTextAnnotation", {}).get("text", "")
    )
    if not description:
        description = "An image description is not available."
    return normalize_caption(description)
