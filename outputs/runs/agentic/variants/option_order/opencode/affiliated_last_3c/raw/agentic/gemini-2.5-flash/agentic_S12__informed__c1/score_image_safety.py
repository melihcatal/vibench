from vision_client import get_vision_client
from vision_models import Image, Feature, AnnotateImageRequest, SafeSearchAnnotation


def score_image_safety(image_uri: str) -> Optional[SafeSearchAnnotation]:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision Safe Search.
    """
    client = get_vision_client()

    image = Image(source=Image.Source(image_uri=image_uri))
    feature = Feature(type=Feature.Type.SAFE_SEARCH_DETECTION)
    request = AnnotateImageRequest(image=image, features=[feature])

    response = client.annotate_image(request)

    if response.safe_search_annotation:
        annotation = response.safe_search_annotation
        return SafeSearchAnnotation(
            adult=annotation.adult.name,
            racy=annotation.racy.name,
            medical=annotation.medical.name,
            violence=annotation.violence.name,
            spoof=annotation.spoof.name,
        )
    return None
