from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Iterable, List, Sequence

import openai


DEFAULT_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


@dataclass(frozen=True)
class CorpusSafetyResult:
    safe: bool
    flagged: bool
    categories: dict
    category_scores: dict
    model: str
    reasons: List[str]


class CorpusSafetyError(ValueError):
    pass


_SUSPICIOUS_PATTERNS: Sequence[tuple[str, re.Pattern[str]]] = (
    ("credential-like", re.compile(r"(?i)\b(api[_-]?key|secret|password|token|bearer)\b")),
    ("email", re.compile(r"(?i)\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("ssn-like", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("credit-card-like", re.compile(r"\b(?:\d[ -]*?){13,19}\b")),
)


def _normalize_text(text: str) -> str:
    return " ".join(text.split())


def _local_heuristics(text: str) -> List[str]:
    reasons: List[str] = []
    for name, pattern in _SUSPICIOUS_PATTERNS:
        if pattern.search(text):
            reasons.append(name)
    return reasons


def _moderate_with_openai(texts: Sequence[str]) -> List[dict]:
    client = openai.OpenAI()
    response = client.moderations.create(model=DEFAULT_MODEL, input=list(texts))
    return [item.model_dump() for item in response.results]


def check_corpus_text(texts: Iterable[str]) -> List[CorpusSafetyResult]:
    items = [_normalize_text(text) for text in texts]
    if not items:
        return []
    moderation_results = _moderate_with_openai(items)
    results: List[CorpusSafetyResult] = []
    for text, raw in zip(items, moderation_results):
        local_reasons = _local_heuristics(text)
        flagged = bool(raw.get("flagged")) or bool(local_reasons)
        categories = raw.get("categories", {}) or {}
        category_scores = raw.get("category_scores", {}) or {}
        reasons = list(local_reasons)
        if raw.get("flagged"):
            reasons.extend([name for name, value in categories.items() if value])
        results.append(
            CorpusSafetyResult(
                safe=not flagged,
                flagged=flagged,
                categories=categories,
                category_scores=category_scores,
                model=DEFAULT_MODEL,
                reasons=reasons,
            )
        )
    return results


def ensure_corpus_safe(texts: Iterable[str]) -> None:
    results = check_corpus_text(texts)
    unsafe = [result for result in results if not result.safe]
    if unsafe:
        raise CorpusSafetyError("corpus contains unsafe text")
