from __future__ import annotations

from typing import Optional

from speech_client import SpeechClientConfig, build_assemblyai_client, resolve_audio_source
from speech_models import SubmitTranscriptionRequest, TranscriptionJob


def diarized_transcript(audio_path: Optional[str] = None, *, audio_url: Optional[str] = None) -> TranscriptionJob:
    config = SpeechClientConfig.from_env()
    client = build_assemblyai_client(config)
    source = resolve_audio_source(audio_path=audio_path, audio_url=audio_url)
    request = SubmitTranscriptionRequest(source=source, diarization=True, word_timestamps=True)
    transcript = client.transcripts.transcribe(request.to_assemblyai_payload())
    return TranscriptionJob.from_assemblyai(transcript)
