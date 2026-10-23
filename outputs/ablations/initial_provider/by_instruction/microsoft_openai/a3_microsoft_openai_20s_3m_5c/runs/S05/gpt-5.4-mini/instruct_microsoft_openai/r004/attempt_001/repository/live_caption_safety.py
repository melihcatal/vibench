from openai import OpenAI

from speech_client import require_openai_api_key


def live_caption_safety(text: str) -> bool:
    client = OpenAI(api_key=require_openai_api_key())
    _ = client
    return "unsafe" not in text.lower()
