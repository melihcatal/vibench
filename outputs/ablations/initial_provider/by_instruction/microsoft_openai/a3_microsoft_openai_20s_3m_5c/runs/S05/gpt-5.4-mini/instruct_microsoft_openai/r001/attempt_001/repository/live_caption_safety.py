from openai import OpenAI

from speech_client import create_openai_client, load_speech_config


def check_live_caption_safety(text: str) -> str:
    config = load_speech_config()
    client: OpenAI = create_openai_client(config)
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return str(getattr(response, "results", []))
