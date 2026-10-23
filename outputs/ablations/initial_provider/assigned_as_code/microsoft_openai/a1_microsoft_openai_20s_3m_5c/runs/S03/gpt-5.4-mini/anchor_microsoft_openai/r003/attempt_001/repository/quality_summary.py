import requests

from translation_client import build_headers, load_translation_config, translation_url


def quality_summary(payload, config=None):
    cfg = load_translation_config(config)
    response = requests.post(
        translation_url(cfg, "/translate"),
        headers=build_headers(cfg),
        params={"api-version": "3.0", "from": payload["source_language"], "to": payload["target_language"], "toScript": "Latn"},
        json=[{"Text": payload["translated_text"]}],
        timeout=30,
    )
    response.raise_for_status()
    return {"issues": [response.json()[0]["translations"][0]["text"]], "source_language": payload["source_language"], "target_language": payload["target_language"]}
