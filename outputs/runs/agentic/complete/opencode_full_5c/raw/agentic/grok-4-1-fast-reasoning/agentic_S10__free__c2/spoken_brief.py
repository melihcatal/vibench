from model_client import get_openai_client
import os


def spoken_brief(
    text: str, voice: str = "alloy", output_file: str = "spoken_brief.mp3"
) -> str:
    client = get_openai_client()
    speech = client.audio.speech.create(model="tts-1", voice=voice, input=text[:4000])
    speech.stream_to_file(output_file)
    return output_file
