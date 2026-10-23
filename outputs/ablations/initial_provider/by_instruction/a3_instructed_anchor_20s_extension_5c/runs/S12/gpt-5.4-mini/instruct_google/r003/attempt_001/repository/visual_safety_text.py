from typing import Iterable


def visual_safety_text(labels: Iterable[str]) -> bool:
    unsafe_terms = {"weapon", "blood", "nude", "nsfw", "gore"}
    normalized = {label.lower() for label in labels if label}
    return any(term in normalized for term in unsafe_terms)
