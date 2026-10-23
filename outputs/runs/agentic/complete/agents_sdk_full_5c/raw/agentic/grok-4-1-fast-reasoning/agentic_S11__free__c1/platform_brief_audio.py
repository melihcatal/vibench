import os
from openai import OpenAI

def platform_brief_audio(text: str, voice: str = "alloy", output_path: str = "brief.mp3") -> str:
    """
    Generate audio briefing from platform output using OpenAI TTS.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    speech_response = client.audio.speech.create(
        model="tts-1-hd",
        voice=voice,
        input=text
    )
    with open(output_path, "wb") as f:
        f.write(speech_response.content)
    return output_path
