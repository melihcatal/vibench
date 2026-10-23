import os
from typing import Any, Dict, Optional

from openai import OpenAI


def submit_transcription(audio_file_path: str, language: Optional[str] = None, prompt: Optional[str] = None, model: str = "gpt-4o-transcribe") -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language=language,
            prompt=prompt,
        )
    if hasattr(transcription, "model_dump"):
        return transcription.model_dump()
    return transcription.to_dict() if hasattr(transcription, "to_dict") else dict(transcription)
