from openai import OpenAI


def generate_reviewer_brief_audio(
    text: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts"
):
    client = OpenAI()
    response = client.audio.speech.create(model=model, voice=voice, input=text)
    return response.content
