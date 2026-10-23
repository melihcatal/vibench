import json
import os
from pathlib import Path

from openai import OpenAI


def submit_transcription(audio_file_path: str, *, model: str = "gpt-4o-transcribe", language: str | None = None, prompt: str | None = None, timeout: float | None = None) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=timeout)
    path = Path(audio_file_path)
    with path.open("rb") as audio_file:
        kwargs = {"model": model, "file": audio_file}
        if language is not None:
            kwargs["language"] = language
        if prompt is not None:
            kwargs["prompt"] = prompt
        response = client.audio.transcriptions.create(**kwargs)
    return json.loads(response.model_dump_json())
