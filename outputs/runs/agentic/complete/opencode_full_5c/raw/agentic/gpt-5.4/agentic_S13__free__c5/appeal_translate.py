from __future__ import annotations

import requests

from safety_client import deepl_config


def appeal_translate(text: str, target_language: str = "EN") -> str:
    config = deepl_config()
    response = requests.post(
        config["endpoint"],
        headers={"Authorization": f"DeepL-Auth-Key {config['api_key']}"},
        data={"text": text, "target_lang": target_language},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["translations"][0]["text"]
