from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from speech_client import get_openai_client, resolve_transcription_model
from speech_models import TranscriptResult


def transcribe_qa_audio(
    audio_path: Union[str, Path],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> TranscriptResult:
    resolved_model = resolve_transcription_model(model)
    client = get_openai_client(api_key)
    path = Path(audio_path)
    with path.open("rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=resolved_model, file=audio_file
        )
    transcript = (
        response.text if hasattr(response, "text") else response.get("text", "")
    )
    return TranscriptResult(transcript=transcript, model=resolved_model)
