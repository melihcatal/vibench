import json
import os
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Mapping

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "omni-moderation-latest"


def _extract_results(payload: Mapping[str, Any]) -> List[Dict[str, Any]]:
    output = payload.get("output", [])
    if not isinstance(output, list):
        return []
    results: List[Dict[str, Any]] = []
    for item in output:
        if not isinstance(item, dict):
            continue
        for content_item in item.get("content", []):
            if isinstance(content_item, dict):
                extracted = content_item.get("results", [])
                if isinstance(extracted, list):
                    for result in extracted:
                        if isinstance(result, dict):
                            results.append(result)
    return results


def _label_for_result(result: Mapping[str, Any]) -> str:
    for key in ("label", "verdict", "safety_label", "decision"):
        value = result.get(key)
        if value is not None:
            return str(value).strip().lower()
    flagged = result.get("flagged")
    if isinstance(flagged, bool):
        return "unsafe" if flagged else "safe"
    return "unknown"


def _aggregate_results(results: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    counts = Counter()
    category_counts: Dict[str, Counter] = defaultdict(Counter)
    confidences: List[float] = []

    for result in results:
        label = _label_for_result(result)
        counts[label] += 1
        confidence = result.get("confidence", result.get("score"))
        try:
            if confidence is not None:
                confidences.append(float(confidence))
        except (TypeError, ValueError):
            pass

        categories = result.get("categories", result.get("category_scores", []))
        if isinstance(categories, list):
            for category in categories:
                if not isinstance(category, Mapping):
                    continue
                name = str(category.get("category", category.get("name", "unknown"))).strip().lower()
                flagged = category.get("flagged")
                if isinstance(flagged, bool):
                    category_counts[name]["flagged" if flagged else "clear"] += 1
                else:
                    category_counts[name]["seen"] += 1

    total = sum(counts.values())
    summary = {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "total": total,
        "labels": dict(counts),
        "average_confidence": round(sum(confidences) / len(confidences), 4) if confidences else 0.0,
        "categories": {key: dict(value) for key, value in category_counts.items()},
    }
    return summary


def summarize_moderation_decisions(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    return _aggregate_results(results)


def summarize_from_openai(messages: List[str]) -> Dict[str, Any]:
    api_key = os.environ["OPENAI_API_KEY"]
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_MODEL, "input": messages},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return summarize_moderation_decisions(_extract_results(data))


def main() -> None:
    import sys

    payload = json.loads(sys.stdin.read() or "[]")
    if isinstance(payload, list):
        result = summarize_from_openai([str(item) for item in payload])
    elif isinstance(payload, dict):
        result = summarize_moderation_decisions(payload.get("results", []))
    else:
        result = summarize_moderation_decisions([])
    print(json.dumps(result))


if __name__ == "__main__":
    main()
