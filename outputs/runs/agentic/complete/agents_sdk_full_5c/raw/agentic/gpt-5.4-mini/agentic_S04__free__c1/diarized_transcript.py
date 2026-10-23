from __future__ import annotations

from openai import OpenAI

from speech_client import get_client
from speech_models import TranscriptionJobRequest, extract_transcript_fields


def diarized_transcript(audio_path: str, language: str | None = None) -> dict:
    client: OpenAI = get_client()
    request = TranscriptionJobRequest(audio_path=audio_path, language=language, speaker_diarization=True)
    with open(request.audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=request.model,
            file=audio_file,
            language=request.language,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )
    result = extract_transcript_fields(transcript)
    diarized_segments = []
    for segment in result.segments:
        diarized_segments.append(
            {
                "speaker": segment.get("speaker", segment.get("speaker_id", "unknown")),
                "start": segment.get("start"),
                "end": segment.get("end"),
                "text": segment.get("text", ""),
            }
        )
    return {"text": result.text, "segments": diarized_segments, "raw": result.raw}
