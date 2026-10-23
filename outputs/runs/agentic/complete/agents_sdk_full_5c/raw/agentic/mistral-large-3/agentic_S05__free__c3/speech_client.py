import os
from openai import AsyncOpenAI

def get_speech_client():
    return AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def streaming_recognize(config: dict):
    client = get_speech_client()
    return await client.audio.transcriptions.create(
        model=config["model"],
        language=config.get("language"),
        response_format=config.get("response_format", "text"),
        punctuation=config.get("punctuation", True),
        stream=True
    )