from openai import OpenAI

from speech_client import load_speech_config


def check_live_caption_safety(text: str) -> str:
    config = load_speech_config()
    client = OpenAI(api_key=config.api_key or None)
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    if result.flagged:
        return "unsafe"
    return "safe"
