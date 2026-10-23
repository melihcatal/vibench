import requests

from speech_client import auth_headers, build_endpoint, load_config


def select_voice(locale: str):
    cfg = load_config()
    endpoint = f"https://{cfg.region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
    response = requests.get(endpoint, headers={'Ocp-Apim-Subscription-Key': cfg.api_key}, timeout=60)
    response.raise_for_status()
    voices = response.json()
    return [v for v in voices if v.get('Locale', '').lower().startswith((locale or '').lower())]
