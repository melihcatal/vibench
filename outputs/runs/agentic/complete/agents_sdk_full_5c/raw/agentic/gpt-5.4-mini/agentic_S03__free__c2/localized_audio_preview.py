from openai import OpenAI

from translation_client import load_config

OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TTS_VOICE = "alloy"


def generate_audio_preview(text: str, language: str) -> bytes:
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key) if cfg.api_key else OpenAI()
    prompt = f"Read this in {language} naturally: {text}"
    audio = client.audio.speech.create(model=OPENAI_TTS_MODEL, voice=OPENAI_TTS_VOICE, input=prompt)
    return audio.read()
