from vision_client import get_vision_client
from vision_models import LocalizedObjectAnnotation
from google.cloud import vision
from typing import List, Optional


def describe_image(image_uri: str) -> Optional[str]:
    """
    Generates a short description for an image by identifying objects.

    Args:
        image_uri: The URI of the image (e.g., "gs://..." or "http://...").

    Returns:
        A string description of the objects in the image, or None.
    """
    client = get_vision_client()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.object_localization(image=image)

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    if not response.localized_object_annotations:
        return None

    object_names = [obj.name for obj in response.localized_object_annotations]

    if len(object_names) == 0:
        return "No objects detected in the image."
    elif len(object_names) == 1:
        return f"This image contains a {object_names[0]}."
    else:
        # Create a grammatically correct list
        first_objects = ", ".join(object_names[:-1])
        last_object = object_names[-1]
        return f"This image contains {first_objects}, and a {last_object}."
