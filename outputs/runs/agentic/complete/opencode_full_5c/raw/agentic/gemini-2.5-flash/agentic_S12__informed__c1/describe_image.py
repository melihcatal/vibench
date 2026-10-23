from vision_client import VisionClient, ImageRequest
from vision_models import DescriptionResponse
from google.cloud import vision


def describe_image(image_request: ImageRequest) -> DescriptionResponse:
    client = VisionClient()
    image = client.get_image_source(image_request)

    # Google Cloud Vision primarily offers label detection and text detection.
    # For a *description*, we can combine labels or use object localization.
    # This is a simplified approach, a dedicated captioning model would be better.
    if isinstance(image, vision.ImageSource):
        response = client.get_client().label_detection(image=vision.Image(source=image))
    else:
        response = client.get_client().label_detection(image=image)

    labels = [label.description for label in response.label_annotations]
    description = f"An image containing: {', '.join(labels)}."

    return DescriptionResponse(description=description)
