from openai import OpenAI


def reviewer_brief_audio(text: str):
    client = OpenAI()
    return client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
