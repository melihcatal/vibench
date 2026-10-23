from typing import Optional

from speech_client import (
    get_transcription_result,
    submit_transcription_job,
    upload_audio_file,
)
from speech_models import (
    TimestampedSegment,
    TranscriptionResult,
    Utterance,
    WordInfo,
)


def get_timestamped_transcript(
    transcript_id: str,
) -> list[TimestampedSegment]:
    response = get_transcription_result(transcript_id)
    result = TranscriptionResult.from_assemblyai_response(response)

    segments = []
    for utterance in result.utterances:
        segments.append(TimestampedSegment.from_utterance(utterance))

    return segments


def get_word_level_timestamps(
    transcript_id: str,
) -> list[WordInfo]:
    response = get_transcription_result(transcript_id)
    result = TranscriptionResult.from_assemblyai_response(response)
    return result.words


def request_timestamped_transcription(
    audio_file_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    language_code: str = "en",
) -> TranscriptionResult:
    if audio_file_path:
        audio_url = upload_audio_file(audio_file_path)
    elif not audio_url:
        raise ValueError("Either audio_file_path or audio_url must be provided")

    response = submit_transcription_job(
        audio_url=audio_url,
        language_code=language_code,
        word_timestamps=True,
        punctuate=True,
        format_text=True,
    )

    return TranscriptionResult.from_assemblyai_response(response)


def format_timestamped_output(
    segments: list[TimestampedSegment],
) -> str:
    lines = []
    for seg in segments:
        start_sec = seg.start_ms / 1000.0
        end_sec = seg.end_ms / 1000.0
        lines.append(f"[{start_sec:.2f}s - {end_sec:.2f}s] {seg.text}")
    return "\n".join(lines)


def find_segment_at_timestamp(
    segments: list[TimestampedSegment], timestamp_ms: int
) -> Optional[TimestampedSegment]:
    for seg in segments:
        if seg.start_ms <= timestamp_ms <= seg.end_ms:
            return seg
    return None
