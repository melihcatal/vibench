from vision_client import get_vision_client
from vision_models import normalize_labels, normalize_text

def summarize_visual_analysis(labels, text, safety):
    client = get_vision_client()
    normalized_labels = normalize_labels(labels)
    normalized_text = normalize_text(text)
    safety_summary = f'Safety: Adult={safety[0]}, Violence={safety[1]}, Racy={safety[2]}, Medical={safety[3]}, Spoof={safety[4]}'
    return f'Labels: {normalized_labels}, Text: {normalized_text}, {safety_summary}'