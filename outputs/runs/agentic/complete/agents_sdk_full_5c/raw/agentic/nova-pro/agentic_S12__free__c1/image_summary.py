from vision_client import get_vision_client
from vision_models import VisionModel

def summarize_image(image_path):
    client = get_vision_client()
    model = VisionModel()
    labels = detect_labels(client, image_path)
    description = describe_image(client, image_path)
    text = detect_text(client, image_path)
    safety = score_safety(client, image_path)
    summary = model.normalize_response({'labels': labels, 'description': description, 'text': text, 'safety': safety})
    print('Summary:', summary)