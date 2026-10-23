from.vision_client import VisionClient

def image_summary(image_url, endpoint, key):
    client = VisionClient(endpoint, key)
    labels = detect_image_labels(image_url, endpoint, key)
    description = describe_image(image_url, endpoint, key)
    text = detect_image_text(image_url, endpoint, key)
    safety = score_image_safety(image_url, endpoint, key)
    return {
        'labels': labels,
        'description': description,
        'text': text,
        'safety': safety
    }