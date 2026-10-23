import json
from openai import OpenAI

from speech_client import load_config


def diarized_transcript(file_path: str, language: str = None):
    config = load_config("microsoft")
    client = OpenAI(api_key=config.api_key, base_url=config.endpoint)
    with open(file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=config.model,
            file=audio_file,
            language=language,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
    return json.loads(result.model_dump_json())
