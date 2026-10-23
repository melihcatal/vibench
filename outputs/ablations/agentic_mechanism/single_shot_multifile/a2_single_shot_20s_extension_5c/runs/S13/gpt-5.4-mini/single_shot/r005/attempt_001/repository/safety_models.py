from typing import Any, Dict, Iterable, List, Optional, Tuple


def _to_dict(obj: Any) -> Dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return {k: getattr(obj, k) for k in dir(obj) if not k.startswith("_") and not callable(getattr(obj, k))}


def extract_moderation_output(response: Any) -> Dict[str, Any]:
    payload = _to_dict(response)
    results = payload.get("results") or []
    if not results and hasattr(response, "results"):
        results = getattr(response, "results")
    first = _to_dict(results[0]) if results else {}
    categories = first.get("categories") or {}
    category_scores = first.get("category_scores") or first.get("category_scores", {})
    flagged = bool(first.get("flagged", False))
    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": payload,
    }


def build_moderation_result(provider: str, operation: str, input_text: str, input_type: str, moderation: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "provider": provider,
        "operation": operation,
        "input_type": input_type,
        "input_text": input_text,
        "flagged": bool(moderation.get("flagged", False)),
        "categories": moderation.get("categories", {}),
        "category_scores": moderation.get("category_scores", {}),
        "metadata": metadata or {},
    }


def build_batch_result(provider: str, operation: str, items: List[Dict[str, Any]], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "provider": provider,
        "operation": operation,
        "items": items,
        "metadata": metadata or {},
    }


def redact_text_from_categories(text: str, categories: Dict[str, Any]) -> Tuple[str, List[Dict[str, Any]]]:
    if not categories:
        return text, []
    spans: List[Dict[str, Any]] = []
    redacted = text
    if any(bool(v) for v in categories.values()):
        spans.append({"start": 0, "end": len(text), "label": "unsafe"})
        redacted = "[REDACTED]"
    return redacted, spans


def build_redaction_result(provider: str, operation: str, input_text: str, redacted_text: str, spans: List[Dict[str, Any]], moderation: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "provider": provider,
        "operation": operation,
        "input_text": input_text,
        "redacted_text": redacted_text,
        "spans": spans,
        "flagged": bool(moderation.get("flagged", False)),
        "categories": moderation.get("categories", {}),
        "category_scores": moderation.get("category_scores", {}),
        "metadata": metadata or {},
    }


def threshold_decision(category_scores: Dict[str, Any], thresholds: Dict[str, float]) -> Dict[str, Any]:
    triggered = []
    for category, threshold in thresholds.items():
        score = float(category_scores.get(category, 0.0) or 0.0)
        if score >= threshold:
            triggered.append({"category": category, "score": score, "threshold": threshold})
    allow = len(triggered) == 0
    return {"allow": allow, "triggered": triggered}


def build_threshold_result(provider: str, operation: str, input_text: str, moderation: Dict[str, Any], thresholds: Dict[str, float], decision: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {
        "provider": provider,
        "operation": operation,
        "input_text": input_text,
        "flagged": bool(moderation.get("flagged", False)),
        "categories": moderation.get("categories", {}),
        "category_scores": moderation.get("category_scores", {}),
        "thresholds": thresholds,
        "decision": decision,
        "metadata": metadata or {},
    }
