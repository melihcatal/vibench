import os
import requests

from speech_client import load_speech_config


def translate_transcript(payload, config=None):
    cfg = load_speech_config(config)
    target_language = (config or {}).get("target_language") or os.environ.get("TARGET_LANGUAGE", "en")
    response = requests.post(
        "https://api.cognitive.microsofttranslator.com/translate",
        params={"api-version": "3.0", "to": target_language},
        headers={
            "Ocp-Apim-Subscription-Key": cfg.api_key,
            "Ocp-Apim-Subscription-Region": cfg.region,
            "Content-Type": "application/json",
        },
        json=[{"text": payload["text"]}],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
