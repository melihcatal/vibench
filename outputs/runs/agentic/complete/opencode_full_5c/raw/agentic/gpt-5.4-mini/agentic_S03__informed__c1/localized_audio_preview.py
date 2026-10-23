from openai import OpenAI


def localized_audio_preview(text: str) -> bytes:
    client = OpenAI()
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=text
    )
    return response.read()
