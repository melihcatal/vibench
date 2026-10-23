from [SAME-SCENARIO] detect_image_labels import detect_image_labels
from [SAME-SCENARIO] describe_image import describe_image
from [SAME-SCENARIO] detect_image_text import detect_image_text
from [SAME-SCENARIO] score_image_safety import score_image_safety


def summarize_visual_analysis(payload, config=None):
    labels = detect_image_labels(payload, config)
    description = describe_image(payload, config)
    text = detect_image_text(payload, config)
    safety_score = score_image_safety(payload, config)
    return {
        'labels': labels,
        'description': description,
        'text': text,
        'safety_score': safety_score
    }