from __future__ import annotations

from typing import Iterable

from vision_models import SafetyScore


def check_generated_visual_labels_for_unsafe_text(labels: Iterable[str]) -> bool:
    banned = {"nudity", "explicit", "weapon", "violence", "blood", "gore"}
    for label in labels:
        token = label.lower().strip()
        if any(word in token for word in banned):
            return True
    return False


def derive_text_risk_from_safety(score: SafetyScore) -> str:
    if score.adult in {"LIKELY", "VERY_LIKELY"} or score.violence in {"LIKELY", "VERY_LIKELY"}:
        return "high"
    if score.racy in {"LIKELY", "VERY_LIKELY"}:
        return "medium"
    return "low"


__all__ = ["check_generated_visual_labels_for_unsafe_text", "derive_text_risk_from_safety"]
