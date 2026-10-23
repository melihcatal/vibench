from vision_client import VisionClient
from vision_models import construct_image_source, parse_label_detection_response
from google.cloud import vision_v1


def describe_image(image_uri=None, image_content=None):
    client = VisionClient().image_annotator_client
    image = vision_v1.Image(source=construct_image_source(image_uri, image_content))

    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.LABEL_DETECTION)]
    request = vision_v1.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request=request)

    labels_data = parse_label_detection_response(response)
    if labels_data and labels_data["labels"]:
        return {"description": " ".join(labels_data["labels"])}
    return {"description": "No clear description available."}
