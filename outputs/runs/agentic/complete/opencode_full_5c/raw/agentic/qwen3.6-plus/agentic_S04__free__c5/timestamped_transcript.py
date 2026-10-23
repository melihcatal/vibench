from typing import Optional
import httpx
from speech_client import (
    OPENAI_API_KEY,
    TRANSCRIPTION_ENDPOINT,
    get_headers,
    validate_api_key,
    build_audio_payload,
    extract_segments_from_response,
    extract_words_from_response,
)
from speech_models import (
    AudioTranscriptionRequest,
    TimestampedSegment,
    WordTimestamp,
    TranscriptionResult,
    normalize_transcription_response,
)


def get_word_timestamps(
    file_path: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    response_format: str = "verbose_json",
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/octet-stream")}
        data = build_audio_payload(
            audio_file_path=file_path,
            model=model,
            response_format=response_format,
            language=language,
            timestamp_granularities=["word"],
        )
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

        response = httpx.post(
            TRANSCRIPTION_ENDPOINT,
            headers=headers,
            files=files,
            data=data,
            timeout=120.0,
        )
        response.raise_for_status()
        result = response.json()

    return extract_words_from_response(result)


def get_segment_timestamps(
    file_path: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    response_format: str = "verbose_json",
) -> list:
    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/octet-stream")}
        data = build_audio_payload(
            audio_file_path=file_path,
            model=model,
            response_format=response_format,
            language=language,
            timestamp_granularities=["segment"],
        )
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

        response = httpx.post(
            TRANSCRIPTION_ENDPOINT,
            headers=headers,
            files=files,
            data=data,
            timeout=120.0,
        )
        response.raise_for_status()
        result = response.json()

    return extract_segments_from_response(result)


def timestamped_transcript(
    file_path: str,
    model: str = "whisper-1",
    language: Optional[str] = None,
    granularity: str = "word",
) -> TranscriptionResult:
    request = AudioTranscriptionRequest(
        file_path=file_path,
        model=model,
        language=language,
        response_format="verbose_json",
        timestamp_granularities=["word", "segment"],
    )

    if not validate_api_key():
        raise ValueError("OpenAI API key is not set or invalid")

    with open(request.file_path, "rb") as f:
        files = {"file": (request.file_path, f, "application/octet-stream")}
        data = build_audio_payload(
            audio_file_path=request.file_path,
            model=request.model,
            response_format=request.response_format,
            language=request.language,
            timestamp_granularities=request.timestamp_granularities,
        )
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

        response = httpx.post(
            TRANSCRIPTION_ENDPOINT,
            headers=headers,
            files=files,
            data=data,
            timeout=120.0,
        )
        response.raise_for_status()
        result = response.json()

    transcription = normalize_transcription_response(result)

    timestamped = []
    for seg in transcription.segments:
        seg_words = [w for w in transcription.words if seg.start <= w.start < seg.end]
        timestamped.append(
            TimestampedSegment(
                start=seg.start,
                end=seg.end,
                text=seg.text,
                words=seg_words,
            )
        )

    return TranscriptionResult(
        text=transcription.text,
        language=transcription.language,
        duration=transcription.duration,
        segments=timestamped,
        words=transcription.words,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        gran = sys.argv[2] if len(sys.argv) > 2 else "word"
        result = timestamped_transcript(audio_path, granularity=gran)
        print(f"Language: {result.language}")
        print(f"Duration: {result.duration}s")
        for seg in result.segments:
            print(f"[{seg.start:.2f}s-{seg.end:.2f}s] {seg.text}")
    else:
        print(
            "Usage: python timestamped_transcript.py <audio_file_path> [word|segment]"
        )
