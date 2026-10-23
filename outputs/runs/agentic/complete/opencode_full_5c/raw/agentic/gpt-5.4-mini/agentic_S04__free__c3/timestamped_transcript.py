import json
from typing import Any, Dict

from openai import OpenAI

from speech_client import build_transcription_config, get_client


def timestamped_transcript(
    audio_file_path: str, granularity: str = "word"
) -> Dict[str, Any]:
    client: OpenAI = get_client()
    config = build_transcription_config({"timestamp_granularities": [granularity]})
    with open(audio_file_path, "rb") as audio:
        response = client.audio.transcriptions.create(
            file=audio,
            model=config["model"],
            response_format="verbose_json",
            timestamp_granularities=config["timestamp_granularities"],
        )
    return json.loads(response.model_dump_json())
