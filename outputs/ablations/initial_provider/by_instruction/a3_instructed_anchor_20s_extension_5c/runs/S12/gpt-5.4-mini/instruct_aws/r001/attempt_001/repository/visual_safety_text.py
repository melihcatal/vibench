from typing import Dict, List


def visual_safety_text(labels: List[str]) -> Dict[str, object]:
    unsafe = [label for label in labels if any(term in label.lower() for term in ("weapon", "blood", "nude", "violence"))]
    return {"unsafe": bool(unsafe), "matches": unsafe}
