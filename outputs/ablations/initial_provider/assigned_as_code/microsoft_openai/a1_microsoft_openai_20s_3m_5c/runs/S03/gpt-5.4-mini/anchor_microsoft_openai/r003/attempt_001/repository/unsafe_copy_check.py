import requests

from translation_client import build_headers, load_translation_config, translation_url


def unsafe_copy_check(payload, config=None):
    cfg = load_translation_config(config)
    response = requests.post(
        translation_url(cfg, "/translate"),
        headers=build_headers(cfg),
        params={"api-version": "3.0", "from": payload["source_language"], "to": payload["target_language"]},
        json=[{"Text": payload["copy"]}],
        timeout=30,
    )
    response.raise_for_status()
    translated = response.json()[0]["translations"][0]["text"]
    return {"unsafe": any(token in translated.lower() for token in ["error", "danger", "unsafe"]), "translated_copy": translated}
