import os
from typing import Optional, List, Dict, Any

from speech_client import (
    create_assemblyai_session,
    upload_audio_file,
    submit_transcription_job,
    ASSEMBLYAI_MODEL,
)
from speech_models import TranscriptionRequest, TranscriptionResult


def submit_audio_for_transcription(
    audio_path: str,
    language_code: Optional[str] = None,
    word_boost: Optional[List[str]] = None,
    custom_spelling: Optional[List[Dict[str, Any]]] = None,
) -> str:
    session = create_assemblyai_session()

    if audio_path.startswith("http://") or audio_path.startswith("https://"):
        audio_url = audio_path
    else:
        audio_url = upload_audio_file(session, audio_path)

    request = TranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        word_boost=word_boost or [],
        custom_spelling=custom_spelling or [],
        punctuate=True,
        format_text=True,
    )

    config = request.to_assemblyai_payload()
    transcript_id = submit_transcription_job(session, audio_url, config)

    return transcript_id


def submit_transcription(audio_path: str, **kwargs) -> Dict[str, Any]:
    transcript_id = submit_audio_for_transcription(audio_path, **kwargs)
    return {
        "transcript_id": transcript_id,
        "model": ASSEMBLYAI_MODEL,
        "provider": "AssemblyAI",
        "status": "queued",
    }


if __name__ == "__main__":
    import sys

    audio_file = sys.argv[1] if len(sys.argv) > 1 else None
    if not audio_file:
        print("Usage: python submit_transcription.py <audio_file_or_url>")
        sys.exit(1)

    result = submit_transcription(audio_file)
    print(result)
