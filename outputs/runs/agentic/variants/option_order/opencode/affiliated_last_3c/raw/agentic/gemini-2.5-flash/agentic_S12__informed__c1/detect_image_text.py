from vision_client import get_vision_client
from vision_models import Image, Feature, AnnotateImageRequest, TextAnnotation


def detect_image_text(image_uri: str) -> Optional[TextAnnotation]:
    """
    Detects text appearing inside an image using Google Cloud Vision.
    """
    client = get_vision_client()

    image = Image(source=Image.Source(image_uri=image_uri))
    feature = Feature(type=Feature.Type.TEXT_DETECTION)
    request = AnnotateImageRequest(image=image, features=[feature])

    response = client.annotate_image(request)

    if response.text_annotations:
        # The first text annotation is typically the aggregate of all text found
        first_annotation = response.text_annotations[0]
        return TextAnnotation(
            description=first_annotation.description, locale=first_annotation.locale
        )
    return None
