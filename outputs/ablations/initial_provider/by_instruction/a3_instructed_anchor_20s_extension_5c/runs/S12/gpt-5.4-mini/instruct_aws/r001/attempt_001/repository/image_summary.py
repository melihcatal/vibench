from typing import Any, Dict, List

from vision_models import normalize_text_list


def image_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    labels: List[str] = normalize_text_list(results.get("labels", []))
    text: List[str] = normalize_text_list(results.get("text", []))
    return {"summary": "; ".join([", ".join(labels[:5]), ", ".join(text[:5])]).strip("; ,"), "labels": labels, "text": text}
