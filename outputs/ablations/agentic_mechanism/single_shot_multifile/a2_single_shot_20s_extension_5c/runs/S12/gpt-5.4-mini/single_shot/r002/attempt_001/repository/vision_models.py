import json
import re
from typing import Any, Dict, List


_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.S)


def _extract_json(text: str) -> Dict[str, Any]:
    match = _JSON_BLOCK_RE.search(text.strip())
    if not match:
        return {}
    try:
        data = json.loads(match.group(0))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}


def coerce_label_list(text: str, max_labels: int = 8) -> List[str]:
    data = _extract_json(text)
    labels = data.get("labels", []) if isinstance(data, dict) else []
    if isinstance(labels, str):
        labels = [labels]
    if not isinstance(labels, list):
        labels = []
    cleaned = []
    for item in labels:
        if isinstance(item, str):
            value = item.strip()
            if value:
                cleaned.append(value)
        if len(cleaned) >= max_labels:
            break
    if cleaned:
        return cleaned
    fallback = [seg.strip(" -\n\t,.") for seg in re.split(r"[,\n]", text) if seg.strip(" -\n\t,.")]
    return fallback[:max_labels]


def normalize_label_result(labels: List[str], provider: str, model: str) -> Dict[str, Any]:
    return {"provider": provider, "model": model, "labels": labels}


def normalize_description_result(description: str, provider: str, model: str, max_chars: int = 240) -> Dict[str, Any]:
    desc = description.strip()
    if len(desc) > max_chars:
        desc = desc[: max_chars - 1].rstrip() + "…"
    return {"provider": provider, "model": model, "description": desc}


def normalize_text_detection_result(text: str, provider: str, model: str) -> Dict[str, Any]:
    data = _extract_json(text)
    detected = data.get("text", "") if isinstance(data, dict) else ""
    if not isinstance(detected, str):
        detected = str(detected)
    if not detected.strip():
        detected = text.strip()
    return {"provider": provider, "model": model, "text": detected.strip()}


def normalize_safety_result(text: str, provider: str, model: str) -> Dict[str, Any]:
    data = _extract_json(text)
    safe = data.get("safe", None) if isinstance(data, dict) else None
    reasons = data.get("reasons", []) if isinstance(data, dict) else []
    if isinstance(reasons, str):
        reasons = [reasons]
    if not isinstance(reasons, list):
        reasons = []
    reasons = [r for r in reasons if isinstance(r, str) and r.strip()]
    if safe is None:
        safe = True
    return {"provider": provider, "model": model, "safe": bool(safe), "reasons": reasons}
