import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")


def _chat_completions_url() -> str:
    return f"{OPENAI_API_BASE.rstrip('/')}/chat/completions"


def _build_prompt(job_results: Dict[str, Any]) -> str:
    items = job_results.get("items") or job_results.get("results") or []
    total = len(items)
    success = sum(1 for item in items if item.get("status") in {"success", "succeeded", "ok"})
    failed = total - success
    model = job_results.get("model") or OPENAI_EMBEDDING_MODEL
    lines = [
        "Summarize this embedding job for an operator.",
        f"Model: {model}",
        f"Total items: {total}",
        f"Succeeded: {success}",
        f"Failed: {failed}",
    ]
    for idx, item in enumerate(items[:20], start=1):
        text = str(item.get("text", ""))[:120]
        status = item.get("status", "unknown")
        error = item.get("error")
        line = f"{idx}. status={status}; text={text}"
        if error:
            line += f"; error={error}"
        lines.append(line)
    return "\n".join(lines)


def summarize_embedding_job(job_results: Dict[str, Any], max_tokens: int = 220) -> str:
    if not OPENAI_API_KEY:
        items = job_results.get("items") or job_results.get("results") or []
        total = len(items)
        success = sum(1 for item in items if item.get("status") in {"success", "succeeded", "ok"})
        failed = total - success
        return f"Embedding job completed: {success}/{total} succeeded, {failed} failed."

    prompt = _build_prompt(job_results)
    response = requests.post(
        _chat_completions_url(),
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-5.4-mini",
            "messages": [
                {"role": "system", "content": "You summarize embedding job results concisely."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    choices = payload.get("choices", [])
    if not choices:
        return "No summary available."
    message = choices[0].get("message", {})
    return message.get("content", "").strip() or "No summary available."
