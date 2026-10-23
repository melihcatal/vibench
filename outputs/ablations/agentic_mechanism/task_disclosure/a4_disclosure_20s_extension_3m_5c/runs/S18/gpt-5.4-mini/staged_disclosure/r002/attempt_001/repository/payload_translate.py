import os
from typing import Any, Dict, List, Optional

import requests


DEEPL_API_BASE = "https://api-free.deepl.com/v2/translate"


def _collect_text_fields(payload: Any, paths: Optional[List[str]] = None) -> Dict[str, str]:
    if paths is None:
        paths = []
    collected: Dict[str, str] = {}
    if isinstance(payload, dict):
        for key, value in payload.items():
            current_path = f"{paths[-1]}.{key}" if paths else key
            if isinstance(value, str) and value.strip():
                collected[current_path] = value
            elif isinstance(value, (dict, list)):
                collected.update(_collect_text_fields(value, paths + [key]))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            current_path = f"{paths[-1]}[{index}]" if paths else f"[{index}]"
            if isinstance(value, str) and value.strip():
                collected[current_path] = value
            elif isinstance(value, (dict, list)):
                collected.update(_collect_text_fields(value, paths + [str(index)]))
    return collected


def _set_nested_value(payload: Any, path: str, value: str) -> None:
    parts: List[Any] = []
    buf = ""
    i = 0
    while i < len(path):
        ch = path[i]
        if ch == ".":
            if buf:
                parts.append(buf)
                buf = ""
            i += 1
            continue
        if ch == "[":
            if buf:
                parts.append(buf)
                buf = ""
            j = path.index("]", i)
            parts.append(int(path[i + 1 : j]))
            i = j + 1
            continue
        buf += ch
        i += 1
    if buf:
        parts.append(buf)

    target = payload
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value


def translate_payload(payload: Dict[str, Any], target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("DEEPL_AUTH_KEY")
    if not api_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")

    texts = _collect_text_fields(payload)
    if not texts:
        return payload

    items = list(texts.items())
    params = [("text", text) for _, text in items]
    params.append(("target_lang", target_language))
    if source_language:
        params.append(("source_lang", source_language))

    response = requests.post(
        DEEPL_API_BASE,
        data=params,
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    translated = response.json().get("translations", [])

    if len(translated) != len(items):
        raise RuntimeError("Unexpected translation response")

    for (path, _), entry in zip(items, translated):
        _set_nested_value(payload, path, entry["text"])

    return payload
