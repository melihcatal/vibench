import requests

from translation_client import build_headers, load_translation_config, translation_url


def translate_dictionary_values(payload, config=None):
    cfg = load_translation_config(config)
    translated = {}
    for key, value in payload["values"].items():
        response = requests.post(
            translation_url(cfg, "/translate"),
            headers=build_headers(cfg),
            params={"api-version": "3.0", "from": payload["source_language"], "to": payload["target_language"]},
            json=[{"Text": str(value)}],
            timeout=30,
        )
        response.raise_for_status()
        translated[key] = response.json()[0]["translations"][0]["text"]
    return {
        "values": translated,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
