from __future__ import annotations

import os
from typing import Any, Dict, Optional

from speech_client import SpeechClientConfig, build_assemblyai_client, resolve_audio_source
from speech_models import SubmitTranscriptionRequest, TranscriptionJob


def submit_transcription(
    audio_path: Optional[str] = None,
    *,
    audio_url: Optional[str] = None,
    language_code: Optional[str] = None,
    diarization: bool = False,
    word_timestamps: bool = False,
) -> TranscriptionJob:
    config = SpeechClientConfig.from_env()
    client = build_assemblyai_client(config)
    source = resolve_audio_source(audio_path=audio_path, audio_url=audio_url)

    request = SubmitTranscriptionRequest(
        source=source,
        language_code=language_code,
        diarization=diarization,
        word_timestamps=word_timestamps,
    )
    payload: Dict[str, Any] = request.to_assemblyai_payload()
    transcript = client.transcripts.transcribe(payload)
    return TranscriptionJob.from_assemblyai(transcript)


if __name__ == "__main__":
    audio = os.environ.get("SPEECH_AUDIO_PATH")
    url = os.environ.get("SPEECH_AUDIO_URL")
    result = submit_transcription(audio_path=audio, audio_url=url)
    print(result.to_dict())
