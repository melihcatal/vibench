import json
import os
import sys
from typing import Any, Dict, List

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _read_input() -> Dict[str, Any]:
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        with open(sys.argv[1], "r", encoding="utf-8") as handle:
            return json.load(handle)
    return json.load(sys.stdin)


def _extract_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(payload.get("results"), list):
        return payload["results"]
    if isinstance(payload.get("data"), list):
        return payload["data"]
    if isinstance(payload.get("jobs"), list):
        return payload["jobs"]
    return []


def _summarize(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(items)
    completed = 0
    failed = 0
    processed_tokens = 0
    dimensions = set()
    ids = []
    for item in items:
        status = str(item.get("status", "")).lower()
        if status in {"succeeded", "completed", "done", "success"}:
            completed += 1
        elif status in {"failed", "error", "errored"}:
            failed += 1
        token_count = item.get("token_count") or item.get("tokens") or 0
        try:
            processed_tokens += int(token_count)
        except (TypeError, ValueError):
            pass
        dim = item.get("embedding_dimension") or item.get("dimensions") or item.get("dimension")
        if dim is not None:
            dimensions.add(dim)
        identifier = item.get("id") or item.get("job_id") or item.get("document_id")
        if identifier is not None:
            ids.append(str(identifier))
    return {
        "total_jobs": total,
        "completed_jobs": completed,
        "failed_jobs": failed,
        "processed_tokens": processed_tokens,
        "distinct_dimensions": sorted(dimensions, key=lambda x: str(x)),
        "job_ids": ids,
    }


def _openai_embedding(text: str) -> List[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        f"{OPENAI_API_BASE}/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={"model": OPENAI_EMBEDDING_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["data"][0]["embedding"]


def main() -> None:
    payload = _read_input()
    items = _extract_items(payload)
    summary = _summarize(items)
    summary["provider"] = "openai"
    summary["embedding_model"] = OPENAI_EMBEDDING_MODEL
    summary["summary_embedding"] = _openai_embedding(json.dumps(summary, sort_keys=True))
    json.dump(summary, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
