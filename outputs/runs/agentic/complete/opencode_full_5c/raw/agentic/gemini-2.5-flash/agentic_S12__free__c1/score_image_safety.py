from vision_client import get_vision_client
from vision_models import ImageRequest, SafeSearchDetectionResponse


def score_image_safety(image_request: ImageRequest) -> SafeSearchDetectionResponse:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.

    Args:
        image_request: An ImageRequest object containing the image content or GCS URI.

    Returns:
        A SafeSearchDetectionResponse object with safety scores.
    """
    client = get_vision_client()
    image = (
        client.image(content=image_request.image_content)
        if image_request.image_content
        else client.image(source={"image_uri": image_request.gcs_uri})
    )
    response = client.safe_search_detection(image=image)
    return SafeSearchDetectionResponse.from_vision_response(response)
