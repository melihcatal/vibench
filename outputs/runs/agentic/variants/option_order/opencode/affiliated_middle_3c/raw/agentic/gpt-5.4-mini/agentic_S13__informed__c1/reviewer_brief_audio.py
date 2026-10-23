from openai import OpenAI

client = OpenAI()
MODEL = 'gpt-4o-mini-tts'


def reviewer_brief_audio(text, voice='alloy'):
    response = client.audio.speech.create(model=MODEL, voice=voice, input=text)
    return response.read()
