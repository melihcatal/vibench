from openai import OpenAI


def reviewer_brief_audio(text, voice="alloy", model="gpt-4o-mini-tts"):
    client = OpenAI()
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    return response.content
