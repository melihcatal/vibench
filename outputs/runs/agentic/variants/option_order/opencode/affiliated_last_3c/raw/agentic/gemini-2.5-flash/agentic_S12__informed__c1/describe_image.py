from vision_client import get_vision_client
from vision_models import Image, Feature, AnnotateImageRequest, ImageDescription


def describe_image(image_uri: str) -> ImageDescription:
    """
    Generates a short visual description for an image using Google Cloud Vision labels.
    """
    client = get_vision_client()

    image = Image(source=Image.Source(image_uri=image_uri))
    feature = Feature(type=Feature.Type.LABEL_DETECTION)
    request = AnnotateImageRequest(image=image, features=[feature])

    response = client.annotate_image(request)

    labels = []
    if response.label_annotations:
        labels = [label.description for label in response.label_annotations]

    # Construct a simple description from labels
    description_text = (
        "A picture with " + ", ".join(labels) + "." if labels else "A picture."
    )

    return ImageDescription(labels=labels, text=description_text)
