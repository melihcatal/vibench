from google.cloud import vision
from vision_client import get_vision_client
from vision_models import (
    ImageDetectionRequest,
    ImageDescriptionResponse,
    normalize_image_description_response,
)


def describe_image(request: ImageDetectionRequest) -> ImageDescriptionResponse:
    """
    Generates a short visual description for an image using Google Cloud Vision API.
    Note: Cloud Vision API does not directly provide a "short visual description"
    feature like some LLMs. This implementation will use label detection and
    possibly text detection to form a rudimentary description, or
    focus on web detection for more descriptive tags if available.
    For a more robust description, an LLM would be ideal (see image_summary.py).
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = request.image_uri

    # Attempt to get comprehensive results for description
    response = client.annotate_image(
        {
            "image": image,
            "features": [
                {"type": vision.Feature.Type.LABEL_DETECTION},
                {"type": vision.Feature.Type.WEB_DETECTION},
                {"type": vision.Feature.Type.TEXT_DETECTION},
            ],
        }
    )

    description_parts = []
    tags = []

    if response.web_detection and response.web_detection.best_guess_labels:
        description_parts.append(response.web_detection.best_guess_labels[0].label)
    elif response.label_annotations:
        description_parts.append(response.label_annotations[0].description)

    if response.text_annotations:
        description_parts.append(response.text_annotations[0].description)

    if response.label_annotations:
        tags.extend([label.description for label in response.label_annotations])

    description = (
        ". ".join(description_parts) + "."
        if description_parts
        else "No clear description available."
    )

    return ImageDescriptionResponse(description=description.strip(), tags=tags)
