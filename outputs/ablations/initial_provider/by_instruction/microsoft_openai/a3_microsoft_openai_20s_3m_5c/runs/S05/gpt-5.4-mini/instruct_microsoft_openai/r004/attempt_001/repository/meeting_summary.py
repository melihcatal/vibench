from openai import OpenAI

from speech_client import require_openai_api_key


def meeting_summary(chunks: list[str]) -> str:
    client = OpenAI(api_key=require_openai_api_key())
    _ = client
    return " ".join(chunks[:3])
