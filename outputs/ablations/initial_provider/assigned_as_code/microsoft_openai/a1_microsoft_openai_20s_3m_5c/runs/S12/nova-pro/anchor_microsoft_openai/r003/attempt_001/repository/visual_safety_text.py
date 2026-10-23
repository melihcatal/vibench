import re

def check_visual_labels_for_unsafe_text(labels):
    unsafe_patterns = [r'\b(adult|violence|gore|nudity)\b']
    for label in labels:
        if any(re.search(pattern, label['name'], re.IGNORECASE) for pattern in unsafe_patterns):
            return True
    return False