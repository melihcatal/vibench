from __future__ import annotations

import json
import os
from typing import Any, Dict, Mapping, Optional

from openai import OpenAI


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _to_dict(value: Any) -> Dict[str, Any]:
    if hasattr(value, "model_dump"):
        return dict(value.model_dump())
    if isinstance(value, dict):
        return dict(value)
    return dict(value)


def _thresholds_from_env() -> Dict[str, float]:
    raw = os.getenv("SAFETY_CATEGORY_THRESHOLDS", "")
    if not raw:
        return {}
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("SAFETY_CATEGORY_THRESHOLDS must be a JSON object")
    return {str(key): float(value) for key, value in parsed.items()}


def decide_allow_text(category_scores: Mapping[str, float], thresholds: Optional[Mapping[str, float]] = None) -> Dict[str, Any]:
    effective_thresholds = dict(_thresholds_from_env())
    if thresholds:
        effective_thresholds.update({str(key): float(value) for key, value in thresholds.items()})

    triggered = {}
    allow = True
    for category, threshold in effective_thresholds.items():
        score = float(category_scores.get(category, 0.0))
        if score >= threshold:
            allow = False
            triggered[category] = {"score": score, "threshold": threshold}

    return {"allow": allow, "triggered": triggered, "thresholds": effective_thresholds}


def safety_threshold(text: str, thresholds: Optional[Mapping[str, float]] = None, model: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    moderation_model = model or OPENAI_MODERATION_MODEL
    response = client.moderations.create(model=moderation_model, input=text)
    result = response.results[0]
    categories = _to_dict(result.categories)
    category_scores = _to_dict(result.category_scores)
    decision = decide_allow_text(category_scores, thresholds)

    return {
        "model": moderation_model,
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": category_scores,
        "allow": decision["allow"] and not bool(result.flagged),
        "triggered_thresholds": decision["triggered"],
        "thresholds": decision["thresholds"],
    }


def main() -> None:
    import sys

    text = sys.stdin.read()
    output = safety_threshold(text)
    sys.stdout.write(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
