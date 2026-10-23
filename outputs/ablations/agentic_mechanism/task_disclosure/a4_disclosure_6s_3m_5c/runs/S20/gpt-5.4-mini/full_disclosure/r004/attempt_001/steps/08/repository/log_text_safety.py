import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class LogTextSafetyResult:
    unsafe: bool
    categories: List[str]
    severity: str
    model: str
    raw_response: Dict[str, Any]


def _load_datadog_config(env: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    source = env if env is not None else os.environ
    return {
        "api_base_url": source.get("MANAGED_LOGGING_API_BASE_URL", "https://api.datadoghq.com"),
        "api_key": source.get("DATADOG_API_KEY", source.get("MANAGED_LOGGING_API_KEY", "")),
        "project_id": source.get("MANAGED_LOGGING_PROJECT_ID", ""),
        "timeout_seconds": source.get("MANAGED_LOGGING_TIMEOUT_SECONDS", "30"),
    }


def _build_prompt(text: str, locale: Optional[str] = None) -> str:
    target_locale = locale or "the original locale"
    return (
        "Assess the following support-visible log message text for unsafe content, including harassment, "
        "self-harm, sexual content, violence, hate, or personal data exposure. Return a strict JSON object "
        "with keys unsafe (boolean), categories (array of strings), severity (one of low, medium, high, critical), "
        "and rationale (string). Evaluate for "
        + target_locale
        + ":\n"
        + text
    )


def check_log_text_safety(text: str, locale: Optional[str] = None, env: Optional[Dict[str, str]] = None) -> LogTextSafetyResult:
    config = _load_datadog_config(env)
    timeout = float(config["timeout_seconds"])
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }
    if config["project_id"]:
        headers["X-Project-Id"] = config["project_id"]
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "system",
                "content": "You are a safety reviewer for log messages.",
            },
            {
                "role": "user",
                "content": _build_prompt(text, locale),
            },
        ],
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        f"{config['api_base_url'].rstrip('/')}/v1/responses",
        headers=headers,
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    text_content = ""
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text_content += content.get("text", "")
    parsed = data if isinstance(data, dict) else {}
    if text_content:
        try:
            import json

            parsed = json.loads(text_content)
        except Exception:
            parsed = data
    return LogTextSafetyResult(
        unsafe=bool(parsed.get("unsafe", False)),
        categories=list(parsed.get("categories", [])) if isinstance(parsed.get("categories", []), list) else [],
        severity=str(parsed.get("severity", "low")),
        model=str(data.get("model", "gpt-4.1-mini")),
        raw_response=data,
    )
