from model_client import get_client


def platform_brief_audio(text: str):
    client = get_client()
    return client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )
