import re

from vision_models import normalize_safety_response


def visual_safety_text(payload, config=None):
    text = " ".join(item.get("name", "") for item in payload.get("labels", []))
    unsafe_terms = ["weapon", "violence", "blood", "nudity", "gore"]
    matches = [term for term in unsafe_terms if re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE)]
    return normalize_safety_response({"unsafe": bool(matches), "categories": [{"name": term, "confidence": 1.0} for term in matches], "summary": ", ".join(matches)})
