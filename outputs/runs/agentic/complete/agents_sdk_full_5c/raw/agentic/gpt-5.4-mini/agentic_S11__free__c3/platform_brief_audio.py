from pathlib import Path

from openai import OpenAI

from model_client import build_client, load_config


def generate_platform_brief_audio(text: str, output_path: str = "briefing.mp3") -> str:
    config = load_config()
    client: OpenAI = build_client(config)
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
    )
    path = Path(output_path)
    speech.stream_to_file(path)
    return str(path)
