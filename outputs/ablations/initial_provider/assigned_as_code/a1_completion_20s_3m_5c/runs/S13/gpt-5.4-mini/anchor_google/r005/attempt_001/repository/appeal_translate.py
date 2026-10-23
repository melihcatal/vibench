import requests


def appeal_translate(payload, config=None):
    config = config or {}
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params={"key": config.get("api_key")},
        json={"q": payload.get("text", ""), "target": config.get("target_language", "en")},
        timeout=30,
    )
    response.raise_for_status()
    return {"translation": response.json()}
