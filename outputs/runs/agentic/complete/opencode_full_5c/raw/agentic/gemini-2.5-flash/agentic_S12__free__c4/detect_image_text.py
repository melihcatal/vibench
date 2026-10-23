from vision_client import get_vision_client, get_image_from_uri, get_image_from_content


def detect_image_text(image_source, is_uri=True):
    client = get_vision_client()
    if is_uri:
        image = get_image_from_uri(image_source)
    else:
        image = get_image_from_content(image_source)

    response = client.text_detection(image=image)
    texts = []
    if response.text_annotations:
        for text in response.text_annotations:
            texts.append(
                {"description": text.description, "bounding_poly": text.bounding_poly}
            )
    return texts
