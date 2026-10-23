from openai import OpenAI


def localized_audio_preview(text, voice="alloy", model="gpt-4o-mini-tts"):
    client = OpenAI()
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    return response
