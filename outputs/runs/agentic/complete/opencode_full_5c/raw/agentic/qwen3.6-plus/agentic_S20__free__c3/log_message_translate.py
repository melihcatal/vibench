import os
import json
import urllib.request
import urllib.error
from typing import Optional

from observability_models import LogEntry


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4o"


def translate_log_messages(
    entries: list[LogEntry],
    target_locale: str = "es",
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> list[dict]:
    results = []
    for entry in entries:
        if not entry.message:
            continue
        translated = _call_openai_translate(
            text=entry.message,
            target_locale=target_locale,
            api_key=api_key,
            model=model,
        )
        results.append(
            {
                "log_id": entry.id,
                "original": entry.message,
                "translated": translated,
                "target_locale": target_locale,
                "model": model,
                "provider": "openai",
            }
        )
    return results


def _call_openai_translate(
    text: str,
    target_locale: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODEL,
) -> str:
    url = f"{OPENAI_API_BASE}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key or OPENAI_API_KEY}",
    }
    system_prompt = (
        f"You are a professional translator. Translate the following log message "
        f"to the {target_locale} locale. Preserve technical terms, variable names, "
        f"and error codes exactly as they appear. Return only the translated text."
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "max_tokens": 512,
        "temperature": 0.1,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = resp.read().decode("utf-8")
            response = json.loads(resp_data)
            return (
                response.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(
            f"OpenAI gpt-4o translation API error {e.code}: {e.reason} - {error_body}"
        ) from e
