"""Request speaker diarization for a recorded meeting using AssemblyAI Transcripts API."""

from typing import Optional

import assemblyai as aai

from speech_client import create_client, normalize_audio_url
from speech_models import TranscriptionRequest, TranscriptionResponse, group_segments_by_speaker


def transcribe_with_diarization(
    audio_input: str,
    language_code: str = "en",
    api_key: Optional[str] = None,
) -> TranscriptionResponse:
    """Transcribe audio with speaker diarization enabled.

    Speaker diarization identifies different speakers in the audio and
    labels each utterance accordingly.

    Args:
        audio_input: URL or local file path to the audio recording.
        language_code: Language code for transcription.
        api_key: Optional AssemblyAI API key; falls back to environment.

    Returns:
        TranscriptionResponse with speaker-labeled segments.
    """
    client = create_client(api_key)
    audio_url = normalize_audio_url(audio_input)

    config = aai.TranscriptionConfig(
        language_code=language_code,
        speaker_labels=True,
        punctuate=True,
        format_text=True,
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Diarized transcription failed: {transcript.error}")

    return TranscriptionResponse.from_assemblyai_transcript(transcript)


def format_diarized_output(
    response: TranscriptionResponse,
    show_timestamps: bool = False,
) -> str:
    """Format diarized transcript segments into a readable meeting transcript."""
    speaker_groups = group_segments_by_speaker(response.segments)
    lines = []
    for speaker_id in sorted(speaker_groups.keys()):
        for seg in speaker_groups[speaker_id]:
            if show_timestamps:
                start_sec = seg.start_ms / 1000
                end_sec = seg.end_ms / 1000
                lines.append(f"[Speaker {speaker_id}] [{start_sec:.1f}s-{end_sec:.1f}s]: {seg.text}")
            else:
                lines.append(f"[Speaker {speaker_id}]: {seg.text}")
    return "\n".join(lines)


def get_meeting_summary_by_speaker(response: TranscriptionResponse) -> dict:
    """Return a summary of who spoke how much in the meeting."""
    speaker_groups = group_segments_by_speaker(response.segments)
    summary = {}
    for speaker_id, segments in speaker_groups.items():
        total_words = sum(len(seg.text.split()) for seg in segments)
        total_duration_ms = sum(seg.end_ms - seg.start_ms for seg in segments)
        summary[f"Speaker {speaker_id}"] = {
            "segments": len(segments),
            "words": total_words,
            "speaking_time_ms": total_duration_ms,
        }
    return summary


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python diarized_transcript.py <audio_url_or_path>")
        sys.exit(1)
    result = transcribe_with_diarization(sys.argv[1])
    print(format_diarized_output(result, show_timestamps=True))
