from vision_client import get_vision_client
from vision_models import normalize_labels, normalize_description, normalize_text, normalize_safety_score

def summarize_visual_analysis(labels, description, text, safety_score):
    summary = {
        'labels': labels,
        'description': description,
        'text': text,
        'safety_score': safety_score
    }
    return summary