import json
from typing import Any, Dict

from openai import OpenAI

from speech_client import build_transcription_config, get_client


def submit_transcription(
    audio_file_path: str, language_code: str | None = None
) -> Dict[str, Any]:
    client: OpenAI = get_client()
    config = build_transcription_config({})
    with open(audio_file_path, "rb") as audio:
        response = client.audio.transcriptions.create(
            file=audio,
            model=config["model"],
            language=language_code,
            response_format="json",
        )
    return json.loads(response.model_dump_json())
