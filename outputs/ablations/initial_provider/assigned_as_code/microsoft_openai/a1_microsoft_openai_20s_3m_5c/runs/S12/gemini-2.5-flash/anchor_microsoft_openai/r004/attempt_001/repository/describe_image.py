from vision_client import VisionClient
from vision_models import create_image_from_bytes, create_feature, parse_label_detection_response, parse_web_detection_response, parse_safe_search_detection_response
from google.cloud import vision

def describe_image(payload, config=None):
    client = VisionClient().get_client()
    image = create_image_from_bytes(payload['image_bytes'])

    features = [
        create_feature(vision.Feature.Type.LABEL_DETECTION, max_results=config.get('max_labels', 10)),
        create_feature(vision.Feature.Type.WEB_DETECTION),
        create_feature(vision.Feature.Type.SAFE_SEARCH_DETECTION)
    ]

    response = client.annotate_image({'image': image, 'features': features})

    labels = parse_label_detection_response(response)
    web_entities = parse_web_detection_response(response)
    safe_search_results = parse_safe_search_detection_response(response)

    description_parts = []
    if labels:
        description_parts.append("Objects detected: " + ", ".join([label['name'] for label in labels[:3]]))
    if web_entities:
        description_parts.append("Likely a " + web_entities[0]['description'] + ".")

    description = " ".join(description_parts).strip()
    if not description and labels:
        description = f"An image containing {labels[0]['name']}."
    elif not description:
        description = "A visual scene."

    return {'description': description, 'safe_search_results': safe_search_results}
