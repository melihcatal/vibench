import os
import json
import urllib.request
import urllib.error
from typing import Optional

from observability_models import LogEntry


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4o"


def summarize_error_logs(
    error_entries: list[LogEntry],
    max_entries: int = 50,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> dict:
    truncated = error_entries[:max_entries]
    log_context = _format_log_entries_for_summary(truncated)
    system_prompt = (
        "You are an incident response analyst. Summarize error log findings "
        "for an incident review. Identify the root cause, affected services, "
        "error patterns, and recommended actions. Be concise and structured."
    )
    user_prompt = (
        f"Analyze the following {len(truncated)} error log entries and provide "
        f"an incident summary:\n\n{log_context}"
    )
    response = _call_openai_chat(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        api_key=api_key,
        model=model,
    )
    return {
        "summary": response.get("choices", [{}])[0]
        .get("message", {})
        .get("content", ""),
        "model": model,
        "provider": "openai",
        "entries_analyzed": len(truncated),
        "total_entries": len(error_entries),
    }


def _format_log_entries_for_summary(entries: list[LogEntry]) -> str:
    lines = []
    for entry in entries:
        line = (
            f"[{entry.timestamp}] {entry.level.upper()} "
            f"service={entry.service} source={entry.source} "
            f"host={entry.hostname} "
            f"correlation_id={entry.correlation_id} "
            f"message={entry.message}"
        )
        lines.append(line)
    return "\n".join(lines)


def _call_openai_chat(
    system_prompt: str,
    user_prompt: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
    max_tokens: int = 2048,
) -> dict:
    url = f"{OPENAI_API_BASE}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or OPENAI_API_KEY}",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(
            f"OpenAI gpt-4o API error {e.code}: {e.reason} - {error_body}"
        ) from e
