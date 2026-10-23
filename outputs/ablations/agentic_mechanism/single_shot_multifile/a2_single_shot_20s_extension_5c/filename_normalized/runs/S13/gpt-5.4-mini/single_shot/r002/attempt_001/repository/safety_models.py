from typing import Any, Dict, List, Optional


def normalize_text_input(text: Any) -> str:
    if text is None:
        return ""
    return str(text).strip()


def normalize_text_list(messages: Any) -> List[str]:
    if messages is None:
        return []
    return [normalize_text_input(m) for m in messages]


def _extract_result(resp: Any) -> Any:
    return resp.results[0] if getattr(resp, "results", None) else None


def moderation_decision_from_openai(resp: Any, text: str) -> Dict[str, Any]:
    result = _extract_result(resp)
    categories = getattr(result, "categories", {}) if result else {}
    category_scores = getattr(result, "category_scores", {}) if result else {}
    flagged = bool(getattr(result, "flagged", False)) if result else False
    return {"text": text, "flagged": flagged, "categories": dict(categories), "category_scores": dict(category_scores)}


def batch_moderation_from_openai(resp: Any, messages: List[str]) -> Dict[str, Any]:
    outputs = []
    results = getattr(resp, "results", []) or []
    for i, message in enumerate(messages):
        result = results[i] if i < len(results) else None
        categories = getattr(result, "categories", {}) if result else {}
        category_scores = getattr(result, "category_scores", {}) if result else {}
        flagged = bool(getattr(result, "flagged", False)) if result else False
        outputs.append({"message": message, "flagged": flagged, "categories": dict(categories), "category_scores": dict(category_scores)})
    return {"results": outputs}


def redact_spans_from_moderation(resp: Any, text: str) -> Dict[str, Any]:
    result = _extract_result(resp)
    spans = getattr(result, "categories", {}) if result else {}
    redacted = text
    for label, hit in spans.items():
        if hit:
            redacted = redacted.replace(label, "[REDACTED]")
    return {"text": text, "redacted_text": redacted, "flagged": bool(getattr(result, "flagged", False)) if result else False, "categories": dict(spans)}


def threshold_decision_from_moderation(resp: Any, text: str, thresholds: Dict[str, float]) -> Dict[str, Any]:
    result = _extract_result(resp)
    category_scores = getattr(result, "category_scores", {}) if result else {}
    category_scores = dict(category_scores)
    violations = {k: v for k, v in category_scores.items() if float(v) >= float(thresholds.get(k, 1.0))}
    return {"text": text, "allowed": not bool(violations), "violations": violations, "category_scores": category_scores, "thresholds": dict(thresholds)}
