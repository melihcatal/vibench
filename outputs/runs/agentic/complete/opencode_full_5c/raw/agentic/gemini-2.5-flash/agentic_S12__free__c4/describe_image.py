from vision_client import get_vision_client, get_image_from_uri, get_image_from_content


def describe_image(image_source, is_uri=True):
    client = get_vision_client()
    if is_uri:
        image = get_image_from_uri(image_source)
    else:
        image = get_image_from_content(image_source)

    response = client.label_detection(image=image)
    descriptions = [
        label.description for label in response.label_annotations if label.score > 0.7
    ]
    if descriptions:
        return "An image depicting " + ", ".join(descriptions) + "."
    else:
        return "A generic image with no clear description."
