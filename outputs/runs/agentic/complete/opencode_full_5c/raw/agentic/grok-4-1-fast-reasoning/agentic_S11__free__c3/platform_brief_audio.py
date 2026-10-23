import os
import openai


def generate_platform_audio_brief(text: str, voice: str = "alloy") -> bytes:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    speech_response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
    return speech_response.content
