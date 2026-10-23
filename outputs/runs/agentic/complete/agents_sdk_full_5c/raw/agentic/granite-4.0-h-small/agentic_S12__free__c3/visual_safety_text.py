from vision_models import LABEL_FEATURE, SAFE_SEARCH_FEATURE
from vision_client import annotate_image

def check_visual_labels_for_unsafe_text(labels, descriptions):
    """Check extracted visual labels and text descriptions for policy-sensitive terms.
    Returns a dict with combined unsafe flag and a list of offending items.
    """
    unsafe_terms = ["bomb", "weapon", "drugs", "nudity", "violence", "graphic"]
    offending = []
    for label in labels:
        if any(term in label["description"].lower() for term in unsafe_terms):
            offending.append(f"Label: {label['description']} (score {label['score']})")
    for text in descriptions:
        if any(term in text.lower() for term in unsafe_terms):
            offending.append(f"Text: {text}")
    is_unsafe = len(offending) > 0
    return {
        "is_unsafe": is_unsafe,
        "offending_items": offending,
    }
