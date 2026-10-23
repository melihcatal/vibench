import os
from typing import Any, Dict, Optional

from openai import OpenAI

from speech_client import get_openai_client, resolve_audio_path
from speech_models import TranscriptionJobRequest, TranscriptionResult, normalize_transcription_result


def submit_transcription(audio_path: str, model: Optional[str] = None, language: Optional[str] = None, prompt: Optional[str] = None) -> Dict[str, Any]:
    client = get_openai_client()
    req = TranscriptionJobRequest(audio_path=audio_path, model=model, language=language, prompt=prompt)
    with resolve_audio_path(req.audio_path) as path:
        with open(path, "rb") as f:
            kwargs: Dict[str, Any] = {"model": req.model}
            if req.language:
                kwargs["language"] = req.language
            if req.prompt:
                kwargs["prompt"] = req.prompt
            result = client.audio.transcriptions.create(file=f, **kwargs)
    return normalize_transcription_result(result)
