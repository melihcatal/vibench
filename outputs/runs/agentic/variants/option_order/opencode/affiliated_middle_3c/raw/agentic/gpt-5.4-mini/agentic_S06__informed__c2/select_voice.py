import requests

from speech_client import load_config, build_headers


def select_voice(locale: str | None = None) -> list[dict]:
    cfg = load_config()
    response = requests.get(
        f"{cfg.base_url}/voices", headers=build_headers(cfg.api_key), timeout=60
    )
    response.raise_for_status()
    voices = response.json().get("voices", [])
    if locale:
        voices = [v for v in voices if locale.lower() in str(v).lower()]
    return voices
