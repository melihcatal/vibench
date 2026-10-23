from typing import List
from vision_models import ImageLabel


def check_unsafe_labels(labels: List[ImageLabel]) -> List[dict]:
    """Checks generated visual labels for unsafe or policy-sensitive content."""
    unsafe_terms = {
        "weapon",
        "gun",
        "knife",
        "blood",
        "violence",
        "hate",
        "racist",
        "discrimination",
        "drug",
        "alcohol",
        "tobacco",
        "nudity",
        "sexual",
    }

    unsafe_labels = []
    for label in labels:
        if any(term in label.description.lower() for term in unsafe_terms):
            unsafe_labels.append(
                {
                    "description": label.description,
                    "score": label.score,
                    "reason": "Contains policy-sensitive content",
                }
            )

    return unsafe_labels
