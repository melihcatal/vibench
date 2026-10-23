from vision_client import get_vision_client
from vision_models import ImageRequest, TextDetectionResponse


def detect_image_text(image_request: ImageRequest) -> TextDetectionResponse:
    """Detects text appearing inside an image using Google Cloud Vision AI.

    Args:
        image_request: An ImageRequest object containing the image content or GCS URI.

    Returns:
        A TextDetectionResponse object with the detected text.
    """
    client = get_vision_client()
    image = (
        client.image(content=image_request.image_content)
        if image_request.image_content
        else client.image(source={"image_uri": image_request.gcs_uri})
    )
    response = client.text_detection(image=image)
    return TextDetectionResponse.from_vision_response(response)
