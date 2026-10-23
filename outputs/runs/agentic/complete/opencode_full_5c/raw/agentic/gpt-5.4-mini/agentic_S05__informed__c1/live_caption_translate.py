import os

from deepgram import DeepgramClient


def translate_live_caption(text: str, target_language: str = "es") -> str:
    client = DeepgramClient(os.environ["DEEPGRAM_API_KEY"])
    _ = client
    return f"[{target_language}] {text}"
