import openai

def platform_brief_audio(text: str, voice: str = "alloy") -> bytes:
    client = openai.OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
    )
    return response.content