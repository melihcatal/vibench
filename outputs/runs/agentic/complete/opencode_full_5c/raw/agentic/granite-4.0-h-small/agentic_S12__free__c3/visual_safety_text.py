# visual_safety_text.py
# [LATER-STEP]

from typing import List
from vision_models import LabelResponse


def contains_unsafe_labels(labels: List[LabelResponse]) -> bool:
    """Check if any detected label suggests unsafe content.

    This simple heuristic looks for keywords in label names (e.g., 'nude', 'weapon').
    Replace with a call to a dedicated safety model if needed.
    """
    unsafe_keywords = {"nude", "weapon", "blood", "drugs", "violence"}
    for label_batch in labels:
        for label in label_batch.labels:
            name = label.get("name", "").lower()
            if any(kw in name for kw in unsafe_keywords):
                return True
    return False


def flag_unsafe_text(text: str) -> bool:
    """Very simple filter for unsafe words in generated text.

    Real implementation would use a profanity/unsafe-word model or API.
    """
    unsafe_words = {"nude", "weapon", "blood", "drugs", "violence", "hate"}
    for word in text.lower().split():
        if word.strip(".,!?;:\") in unsafe_words:
            return True
    return False
