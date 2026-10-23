from __future__ import annotations
from typing import Any, Dict, Iterable, List


def normalize_text_input(text: str) -> Dict[str, str]:
    if text is None:
        text = ""
    return {"text": str(text)}


def normalize_batch_texts(messages: Iterable[str]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for index, text in enumerate(messages):
        items.append({"index": index, "text": "" if text is None else str(text)})
    return items


def build_text_moderation_result(*, text: str, flagged: bool, categories: Dict[str, Any], category_scores: Dict[str, Any], model: str) -> Dict[str, Any]:
    return {"text": text, "flagged": flagged, "categories": categories, "category_scores": category_scores, "model": model}


def build_batch_moderation_result(*, decisions: List[Dict[str, Any]], model: str) -> Dict[str, Any]:
    return {"decisions": decisions, "model": model}


def build_redaction_result(*, text: str, redacted_text: str, unsafe_spans: List[Dict[str, Any]], flagged: bool, model: str) -> Dict[str, Any]:
    return {"text": text, "redacted_text": redacted_text, "unsafe_spans": unsafe_spans, "flagged": flagged, "model": model}


def build_threshold_decision(*, text: str, allow: bool, triggered: Dict[str, Any], model: str) -> Dict[str, Any]:
    return {"text": text, "allow": allow, "triggered": triggered, "model": model}
