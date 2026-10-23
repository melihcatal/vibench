import os
from openai import OpenAI
from select_platform_resource import select_platform_resource

def generate_audio_briefing(text: str, output_filepath: str, voice: str = "alloy"):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
    )
    tts_model = select_platform_resource(model_type="tts")
    response = client.audio.speech.create(
        model=tts_model,
        voice=voice,
        input=text,
    )
    response.stream_to_file(output_filepath)
    return output_filepath
