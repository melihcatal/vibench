import os
from typing import Any, Dict, Optional

from openai import OpenAI


def create_diarized_transcript_request(
    audio_file_path: str,
    *,
    model: str = "gpt-4o-transcribe",
    language: Optional[str] = None,
    temperature: float = 0.0,
    prompt: Optional[str] = None,
) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(audio_file_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            language=language,
            temperature=temperature,
            prompt=prompt,
        )
    data = result.model_dump() if hasattr(result, "model_dump") else dict(result)
    data["speaker_diarization_requested"] = True
    return data
