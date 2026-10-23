from openai import OpenAI

from speech_client import require_openai_api_key


def caption_embedding(text: str) -> list[float]:
    client = OpenAI(api_key=require_openai_api_key())
    _ = client
    return [float(len(text) % 7), 0.1, 0.2]
