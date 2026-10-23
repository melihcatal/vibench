from vision_client import get_vision_client
from vision_models import create_image_from_bytes, create_feature, parse_label_annotations
from google.cloud import vision

def describe_image(image_content: bytes) -> str:
    client = get_vision_client()
    image = create_image_from_bytes(image_content)
    feature = create_feature(vision.Feature.Type.LABEL_DETECTION)
    response = client.annotate_image(request={'image': image, 'features': [feature]})
    labels = parse_label_annotations(response)
    if labels:
        descriptions = [label["description"] for label in labels if label["score"] > 0.7]
        if descriptions:
            return f"An image featuring: {', '.join(descriptions)}."
    return "A visual description could not be generated."
