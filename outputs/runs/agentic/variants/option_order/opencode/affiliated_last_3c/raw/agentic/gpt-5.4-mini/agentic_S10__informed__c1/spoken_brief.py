from openai import OpenAI

from model_client import get_model_name, get_openai_client


def spoken_brief(text: str) -> str:
    client: OpenAI = get_openai_client()
    response = client.audio.speech.create(
        model=get_model_name("tts"),
        voice="alloy",
        input=text,
    )
    return response.model
