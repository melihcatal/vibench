from openai import OpenAI

from speech_client import load_config


def moderate_transcript(text: str):
    config = load_config("openai")
    client = OpenAI(api_key=config.api_key)
    return client.moderations.create(model="omni-moderation-latest", input=text).model_dump()
