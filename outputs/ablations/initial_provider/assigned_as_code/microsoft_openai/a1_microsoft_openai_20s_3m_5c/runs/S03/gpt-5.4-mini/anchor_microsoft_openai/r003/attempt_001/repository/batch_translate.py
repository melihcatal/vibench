import requests

from translation_client import build_headers, load_translation_config, translation_url
from translation_models import normalize_text_list


def batch_translate(payload, config=None):
    cfg = load_translation_config(config)
    texts = normalize_text_list(payload["texts"])
    response = requests.post(
        translation_url(cfg, "/translate"),
        headers=build_headers(cfg),
        params={"api-version": "3.0", "from": payload["source_language"], "to": payload["target_language"]},
        json=[{"Text": text} for text in texts],
        timeout=30,
    )
    response.raise_for_status()
    translated = response.json()
    return {
        "texts": [item["translations"][0]["text"] for item in translated],
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
