from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import get_client, resolve_audio_input
from speech_models import DiarizedTranscriptionRequest, TranscriptionSubmission


def diarized_transcript(audio_path: str, *, speakers: Optional[int] = None, language: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    client = get_client()
    audio_source = resolve_audio_input(audio_path)
    request = DiarizedTranscriptionRequest(audio_source=audio_source, speakers=speakers, language=language, model=model)
    result = client.transcriptions.submit(request)
    if isinstance(result, TranscriptionSubmission):
        return result.to_dict()
    return result


if __name__ == '__main__':
    raise SystemExit(0)
