import re

import requests

from translation_client import build_headers, load_translation_config, translation_url


TAG_RE = re.compile(r"(<[^>]+>|[^<]+)")


def translate_markup(payload, config=None):
    cfg = load_translation_config(config)
    parts = TAG_RE.findall(payload["markup"])
    translated_parts = []
    for part in parts:
        if part.startswith("<"):
            translated_parts.append(part)
            continue
        if not part.strip():
            translated_parts.append(part)
            continue
        response = requests.post(
            translation_url(cfg, "/translate"),
            headers=build_headers(cfg),
            params={"api-version": "3.0", "from": payload["source_language"], "to": payload["target_language"]},
            json=[{"Text": part}],
            timeout=30,
        )
        response.raise_for_status()
        translated_parts.append(response.json()[0]["translations"][0]["text"])
    return {
        "markup": "".join(translated_parts),
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
