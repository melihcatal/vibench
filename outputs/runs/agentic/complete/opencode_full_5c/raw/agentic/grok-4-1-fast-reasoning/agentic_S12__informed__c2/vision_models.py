from typing import List, Dict, Any


def normalize_labels_response(text: str) -> List[str]:
    return [label.strip() for label in text.split(",") if label.strip()]


def normalize_description(text: str) -> str:
    return text.strip()


def normalize_ocr_text(text: str) -> str:
    return text.strip()


def parse_safety_score(text: str) -> Dict[str, Any]:
    score = 0.0
    text_lower = text.lower()
    if "unsafe" in text_lower or "high" in text_lower:
        score = 0.9
    elif "risk" in text_lower or "medium" in text_lower:
        score = 0.5
    else:
        score = 0.1
    status = "unsafe" if score > 0.5 else "safe"
    return {"risk_score": score, "status": status}


VisionAnalysis = Dict[str, Any]
