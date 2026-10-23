from openai import OpenAI
from model_client import get_openai_config


def generate_platform_brief_audio(text: str, output_path: str):
    config = get_openai_config()
    client = OpenAI(**config)
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
    response.stream_to_file(output_path)
