from.detect_image_labels import detect_image_labels
from.describe_image import describe_image
from.detect_image_text import detect_image_text
from.score_image_safety import score_image_safety

def image_summary(image_path):
    labels = detect_image_labels(image_path)
    description = describe_image(image_path)
    text = detect_image_text(image_path)
    safety = score_image_safety(image_path)
    return {'labels': labels, 'description': description, 'text': text, 'safety': safety}