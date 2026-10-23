from vision_client import get_vision_client
from vision_models import Image, Feature, AnnotateImageRequest, LabelAnnotation


def detect_image_labels(image_uri: str) -> list[LabelAnnotation]:
    """
    Detects labels or objects in a static image using Google Cloud Vision.
    """
    client = get_vision_client()

    image = Image(source=Image.Source(image_uri=image_uri))
    feature = Feature(type=Feature.Type.LABEL_DETECTION)
    request = AnnotateImageRequest(image=image, features=[feature])

    response = client.annotate_image(request)
    labels = []
    if response.label_annotations:
        for label in response.label_annotations:
            labels.append(
                LabelAnnotation(
                    mid=label.mid,
                    description=label.description,
                    score=label.score,
                    topicality_score=label.topicality_score,
                )
            )
    return labels
