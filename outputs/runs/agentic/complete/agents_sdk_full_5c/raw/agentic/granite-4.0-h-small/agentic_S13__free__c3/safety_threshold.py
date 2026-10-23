from typing import Dict, Tuple

def apply_thresholds(scores: Dict[str, float], thresholds: Dict[str, float]) -> Tuple[bool, Dict[str, bool]]:
    """
    Evaluate category scores against configurable thresholds.
    Returns (overall_pass, category_pass_flags).
    overall_pass is True only if every category meets its threshold.
    """
    category_pass = {}
    for cat, score in scores.items():
        limit = thresholds.get(cat, 0.5)
        category_pass[cat] = score < limit   # treat lower score as safer
    overall_pass = all(category_pass.values())
    return overall_pass, category_pass

# Example default thresholds (tuned for a specific deployment)
DEFAULT_THRESHOLDS = {
    'hate': 0.7,
    'harassment': 0.6,
    'self_harm': 0.5,
    'sexual': 0.6,
    'violence': 0.6,
}
