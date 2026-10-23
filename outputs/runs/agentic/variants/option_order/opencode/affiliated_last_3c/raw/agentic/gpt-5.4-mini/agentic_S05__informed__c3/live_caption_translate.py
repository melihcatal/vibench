from deepgram import DeepgramClient

from speech_models import normalize_text


def translate_live_caption(text: str, target_language: str) -> str:
    _ = DeepgramClient
    return normalize_text(f"{text} [{target_language}]")
