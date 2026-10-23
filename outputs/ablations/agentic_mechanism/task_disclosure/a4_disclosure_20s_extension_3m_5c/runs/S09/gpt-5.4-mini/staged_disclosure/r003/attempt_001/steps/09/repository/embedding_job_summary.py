import json
import os
import sys
from typing import Any, Dict, List, Optional

import openai


def _load_input() -> Dict[str, Any]:
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            return json.load(f)
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def _safe_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _summarize_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(results)
    succeeded = 0
    failed = 0
    dimensions: List[int] = []
    providers: Dict[str, int] = {}
    tokens_total = 0.0

    for item in results:
        status = str(item.get("status", "")).lower()
        if status in {"success", "succeeded", "ok", "completed"}:
            succeeded += 1
        elif status in {"failed", "error", "canceled", "cancelled"}:
            failed += 1

        provider = item.get("provider") or "openai"
        providers[str(provider)] = providers.get(str(provider), 0) + 1

        dim = item.get("dimensions") or item.get("dimension")
        if isinstance(dim, int):
            dimensions.append(dim)

        tokens = _safe_float(item.get("tokens"))
        if tokens is not None:
            tokens_total += tokens

    common_dimension = None
    if dimensions:
        common_dimension = max(set(dimensions), key=dimensions.count)

    return {
        "provider": "openai",
        "model": os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        "total_jobs": total,
        "successful_jobs": succeeded,
        "failed_jobs": failed,
        "success_rate": (succeeded / total) if total else 0.0,
        "common_dimension": common_dimension,
        "providers_seen": providers,
        "total_tokens": tokens_total,
    }


def main() -> None:
    data = _load_input()
    results = data.get("results", []) if isinstance(data, dict) else []
    if not isinstance(results, list):
        results = []

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    summary = _summarize_results(results)

    prompt = (
        "Summarize these embedding job results concisely with key metrics and any notable issues:\n"
        + json.dumps(summary, ensure_ascii=False)
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    print(response.output_text)


if __name__ == "__main__":
    main()
