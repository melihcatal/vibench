import json
import urllib.request

from speech_client import load_config


def list_voices(locale: str):
    config = load_config()
    url = f"https://{config.azure_speech_region}.tts.speech.microsoft.com/cognitiveservices/voices/list"
    req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": config.azure_speech_key})
    with urllib.request.urlopen(req) as resp:
        voices = json.loads(resp.read().decode("utf-8"))
    return [voice for voice in voices if locale.lower() in voice.get("Locale", "").lower()]


def select_voice(locale: str):
    voices = list_voices(locale)
    return voices[0]["ShortName"] if voices else "en-US-JennyNeural"
