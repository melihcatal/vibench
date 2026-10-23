from vision_client import get_vision_client
from vision_models import normalize_labels

def summarize_visual_analysis(image_path):
    client = get_vision_client()
    labels = client.detect_labels(image_path)
    normalized_labels = normalize_labels(labels)
    return normalized_labels