import json
import os
from typing import Any, Dict, List

import requests


OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def _load_results(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("results", "items", "records", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _get_text(item: Dict[str, Any]) -> str:
    for key in ("text", "input", "content", "chunk", "document"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return json.dumps(item, sort_keys=True, ensure_ascii=False)


def _summarize_with_openai(texts: List[str]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    joined = "\n".join(f"- {text}" for text in texts[:50])
    prompt = (
        "Summarize these embedding job results concisely. Include counts, notable patterns, "
        "and any obvious anomalies.\n\n" + joined
    )

    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_EMBEDDING_MODEL,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return json.dumps(payload, ensure_ascii=False)


def summarize_embedding_job_results(path: str) -> str:
    records = _load_results(path)
    total = len(records)
    successes = 0
    failures = 0
    dimensions = []
    texts: List[str] = []

    for record in records:
        status = str(record.get("status", "")).lower()
        if status in {"success", "succeeded", "ok", "completed"}:
            successes += 1
        elif status in {"failed", "error", "errored"}:
            failures += 1
        vector = record.get("embedding")
        if isinstance(vector, list):
            dimensions.append(len(vector))
        texts.append(_get_text(record))

    summary = {
        "provider": "openai",
        "model": OPENAI_EMBEDDING_MODEL,
        "total_records": total,
        "successes": successes,
        "failures": failures,
        "embedding_dimensions": sorted(set(dimensions)),
    }

    try:
        summary["llm_summary"] = _summarize_with_openai(texts)
    except Exception as exc:
        summary["llm_summary_error"] = str(exc)

    return json.dumps(summary, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python embedding_job_summary.py <results.json>")
    print(summarize_embedding_job_results(sys.argv[1]))
