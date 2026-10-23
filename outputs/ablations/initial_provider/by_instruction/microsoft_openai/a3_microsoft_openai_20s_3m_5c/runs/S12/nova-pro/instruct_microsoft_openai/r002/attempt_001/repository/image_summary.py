from.vision_models import VisionModels

def image_summary(image_path):
    labels = VisionModels.detect_image_labels(image_path)
    description = VisionModels.describe_image(image_path)
    text = VisionModels.detect_image_text(image_path)
    safety = VisionModels.score_image_safety(image_path)
    return {'labels': labels, 'description': description, 'text': text, 'safety': safety}