from vision_client import get_vision_client
from vision_models import normalize_labels, normalize_description, normalize_text, normalize_safety

def summarize_image(image_path):
    client = get_vision_client()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.label_detection(image=image)
    labels = normalize_labels(response.label_annotations)
    description = normalize_description(response.label_annotations)
    text = normalize_text(response.text_annotations[0].description)
    safety = normalize_safety(response.safe_search_annotation)
    return {'labels': labels, 'description': description, 'text': text, 'safety': safety}