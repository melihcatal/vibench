"""Return word or segment timestamps from a transcription result using AssemblyAI Transcripts API."""

from typing import Optional

import assemblyai as aai

from speech_client import create_client, normalize_audio_url
from speech_models import TranscriptionResponse


def get_timestamped_transcript(
    job_id: str,
    api_key: Optional[str] = None,
) -> TranscriptionResponse:
    """Retrieve a completed transcription with word-level timestamps.

    Args:
        job_id: The transcript job ID from a completed transcription.
        api_key: Optional AssemblyAI API key; falls back to environment.

    Returns:
        TranscriptionResponse with word-level timing data.
    """
    client = create_client(api_key)
    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript(job_id)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    if transcript.status != aai.TranscriptStatus.completed:
        raise RuntimeError(f"Transcription not yet complete, status: {transcript.status}")

    return TranscriptionResponse.from_assemblyai_transcript(transcript)


def transcribe_with_timestamps(
    audio_input: str,
    language_code: str = "en",
    api_key: Optional[str] = None,
) -> TranscriptionResponse:
    """Submit and poll for a transcript with full word timestamps.

    Args:
        audio_input: URL or local file path to the audio.
        language_code: Language code for transcription.
        api_key: Optional AssemblyAI API key; falls back to environment.

    Returns:
        TranscriptionResponse with word-level timing data.
    """
    client = create_client(api_key)
    audio_url = normalize_audio_url(audio_input)

    config = aai.TranscriptionConfig(
        language_code=language_code,
        punctuate=True,
        format_text=True,
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Timestamped transcription failed: {transcript.error}")

    return TranscriptionResponse.from_assemblyai_transcript(transcript)


def format_word_timestamps(response: TranscriptionResponse) -> list:
    """Format word-level timestamps into a list of dicts."""
    return [
        {
            "text": word.text,
            "start_ms": word.start_ms,
            "end_ms": word.end_ms,
            "confidence": word.confidence,
        }
        for word in response.words
        if word.text
    ]


def format_segment_timestamps(response: TranscriptionResponse) -> list:
    """Format segment-level timestamps into a list of dicts."""
    return [
        {
            "text": seg.text,
            "start_ms": seg.start_ms,
            "end_ms": seg.end_ms,
            "speaker": seg.speaker,
        }
        for seg in response.segments
        if seg.text
    ]


def generate_srt(response: TranscriptionResponse) -> str:
    """Generate SRT subtitle format from word timestamps."""
    srt_lines = []
    for i, word in enumerate(response.words, start=1):
        if not word.text:
            continue
        start_time = _ms_to_srt_time(word.start_ms)
        end_time = _ms_to_srt_time(word.end_ms)
        srt_lines.append(f"{i}\n{start_time} --> {end_time}\n{word.text}\n")
    return "\n".join(srt_lines)


def _ms_to_srt_time(ms: int) -> str:
    """Convert milliseconds to SRT timestamp format (HH:MM:SS,mmm)."""
    total_seconds, millis = divmod(ms, 1000)
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python timestamped_transcript.py <audio_url_or_path_or_job_id>")
        sys.exit(1)
    result = transcribe_with_timestamps(sys.argv[1])
    for word_info in format_word_timestamps(result)[:10]:
        print(word_info)
