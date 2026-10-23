from vision_client import get_vision_client, get_image_from_uri, get_image_from_content


def detect_image_labels(image_source, is_uri=True):
    client = get_vision_client()
    if is_uri:
        image = get_image_from_uri(image_source)
    else:
        image = get_image_from_content(image_source)

    response = client.label_detection(image=image)
    labels = []
    for label in response.label_annotations:
        labels.append({"description": label.description, "score": label.score})
    return labels
