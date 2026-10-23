from openai import OpenAI


def reviewer_brief_audio(brief_text: str) -> bytes:
    client = OpenAI()
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=brief_text,
        format="mp3",
    )
    return response.read()
