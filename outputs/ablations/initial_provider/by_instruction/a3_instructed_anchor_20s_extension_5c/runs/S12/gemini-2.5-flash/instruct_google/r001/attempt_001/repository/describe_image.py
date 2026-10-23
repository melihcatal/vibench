from vision_client import get_vision_client
from vision_models import (
    create_image_from_bytes,
    create_feature,
    create_annotate_image_request,
    parse_label_annotations,
    parse_landmark_annotations,
    parse_face_annotations
)
from google.cloud import vision

def describe_image(image_bytes: bytes):
    """Generates a short visual description for an image using Google Cloud Vision API.

    Args:
        image_bytes: The bytes of the image to analyze.

    Returns:
        A string describing the image.
    """
    client = get_vision_client()
    image = create_image_from_bytes(image_bytes)

    features = [
        create_feature(vision.Feature.Type.LABEL_DETECTION, max_results=5),
        create_feature(vision.Feature.Type.LANDMARK_DETECTION, max_results=3),
        create_feature(vision.Feature.Type.FACE_DETECTION, max_results=1)
    ]

    request = create_annotate_image_request(image, features)
    response = client.annotate_image(request)

    description_parts = []

    labels = parse_label_annotations(response)
    if labels:
        description_parts.append("It shows " + ", ".join([label["description"] for label in labels]))

    landmarks = parse_landmark_annotations(response)
    if landmarks:
        description_parts.append("with landmarks like " + ", ".join([landmark["description"] for landmark in landmarks]))

    faces = parse_face_annotations(response)
    if faces:
        description_parts.append(f"and {len(faces)} face(s).")

    if not description_parts:
        return "Unable to generate a description for the image."

    return ". ".join(description_parts) + "."
