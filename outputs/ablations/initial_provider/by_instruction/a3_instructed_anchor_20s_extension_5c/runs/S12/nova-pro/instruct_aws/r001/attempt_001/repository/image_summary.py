from vision_client import VisionClient
from vision_models import VisionModels

def image_summary(image_path):
    client = VisionClient()
    labels = client.detect_labels(image_path)
    text = client.detect_text(image_path)
    safety = client.check_safety(image_path)
    return {
        'Labels': VisionModels.normalize_labels(labels),
        'Text': VisionModels.normalize_text(text),
        'Safety': VisionModels.normalize_safety(safety)
    }