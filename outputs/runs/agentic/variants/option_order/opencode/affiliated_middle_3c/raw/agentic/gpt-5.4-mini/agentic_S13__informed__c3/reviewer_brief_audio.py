from openai import OpenAI

MODEL = "gpt-4o-mini-tts"
VOICE = "alloy"


def reviewer_brief_audio(text: str):
    client = OpenAI()
    speech = client.audio.speech.create(model=MODEL, voice=VOICE, input=text)
    return speech
