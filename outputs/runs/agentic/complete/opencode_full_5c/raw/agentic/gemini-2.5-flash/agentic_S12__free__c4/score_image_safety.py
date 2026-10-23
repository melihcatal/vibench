from vision_client import get_vision_client, get_image_from_uri, get_image_from_content


def score_image_safety(image_source, is_uri=True):
    client = get_vision_client()
    if is_uri:
        image = get_image_from_uri(image_source)
    else:
        image = get_image_from_content(image_source)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_scores = {
        "adult": safe_search_annotation.adult.name,
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }
    return safety_scores
