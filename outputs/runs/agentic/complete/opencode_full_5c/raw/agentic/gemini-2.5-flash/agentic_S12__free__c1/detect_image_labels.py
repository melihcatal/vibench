from vision_client import get_vision_client
from vision_models import ImageRequest, LabelDetectionResponse


def detect_image_labels(image_request: ImageRequest) -> LabelDetectionResponse:
    """Detects labels in a static image using Google Cloud Vision AI.

    Args:
        image_request: An ImageRequest object containing the image content or GCS URI.

    Returns:
        A LabelDetectionResponse object with detected labels.
    """
    client = get_vision_client()
    image = (
        client.image(content=image_request.image_content)
        if image_request.image_content
        else client.image(source={"image_uri": image_request.gcs_uri})
    )
    response = client.label_detection(image=image)
    return LabelDetectionResponse.from_vision_response(response)
