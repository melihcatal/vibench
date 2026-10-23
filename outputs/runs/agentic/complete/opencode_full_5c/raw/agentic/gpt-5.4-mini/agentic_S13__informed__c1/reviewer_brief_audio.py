from openai import OpenAI


def reviewer_brief_audio(text: str) -> bytes:
    client = OpenAI()
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice="alloy", input=text
    )
    return response.read()
