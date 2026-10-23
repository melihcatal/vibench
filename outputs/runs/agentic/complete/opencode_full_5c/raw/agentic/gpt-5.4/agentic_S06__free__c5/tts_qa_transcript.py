from __future__ import annotations

from pathlib import Path

import requests

from speech_client import OPENAI_BASE_URL, build_json_headers
from speech_models import TranscriptResult


def transcribe_qa_sample(
    audio_path: str | Path, language: str | None = None
) -> TranscriptResult:
    path = Path(audio_path)
    with path.open("rb") as audio_file:
        files = {"file": (path.name, audio_file, "audio/mpeg")}
        data = {"model": "gpt-4o-mini-transcribe"}
        if language:
            data["language"] = language
        response = requests.post(
            f"{OPENAI_BASE_URL}/audio/transcriptions",
            headers={"Authorization": build_json_headers("openai")["Authorization"]},
            files=files,
            data=data,
            timeout=120,
        )
        response.raise_for_status()
    payload = response.json()
    return TranscriptResult(
        transcript=payload.get("text", ""),
        language=language,
        provider="openai",
    )
