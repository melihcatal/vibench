import base64
from vision_client import VisionClient
from vision_models import normalize_labels_response, normalize_image_description
from google.cloud.vision_v1p4beta1 import Image, Feature  # Provider-identifying signal


def describe_image(image_content: bytes) -> dict:
    client = VisionClient().get_client()
    image = Image(content=image_content)
    feature = Feature(type=Feature.Type.LABEL_DETECTION)
    response = client.annotate_image({"image": image, "features": [feature]})
    labels = normalize_labels_response(response)
    description = normalize_image_description(labels)
    return {"description": description}
