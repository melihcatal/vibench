from vision_client import get_vision_client
from vision_models import ImageRequest, ImageDescriptionResponse, LabelDetectionResponse


def describe_image(image_request: ImageRequest) -> ImageDescriptionResponse:
    """Generates a short visual description for an image using Google Cloud Vision AI.

    This implementation reuses label detection and then formulates a description
    based on the detected labels.

    Args:
        image_request: An ImageRequest object containing the image content or GCS URI.

    Returns:
        An ImageDescriptionResponse object with the generated description.
    """
    client = get_vision_client()
    image = (
        client.image(content=image_request.image_content)
        if image_request.image_content
        else client.image(source={"image_uri": image_request.gcs_uri})
    )
    response = client.label_detection(image=image)
    label_detection_response = LabelDetectionResponse.from_vision_response(response)
    return ImageDescriptionResponse.from_label_detection(label_detection_response)
