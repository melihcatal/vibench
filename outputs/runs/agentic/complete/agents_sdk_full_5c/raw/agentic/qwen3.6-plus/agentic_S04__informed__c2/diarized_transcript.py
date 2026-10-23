"""
[SAME-SCENARIO] Request speaker diarization for a recorded meeting.

Submits an audio file for batch transcription with AssemblyAI speaker
diarization enabled, then polls and returns speaker-labeled utterances.
Provider: AssemblyAI Transcripts API
SDK: assemblyai
Auth: ASSEMBLYAI_API_KEY
"""

import os
from typing import Optional

from speech_client import (
    get_assemblyai_client,
    build_transcription_request,
    upload_local_audio,
    poll_with_retry,
)
from speech_models import normalize_assemblyai_response, TranscriptResponse, Utterance


def diarize_meeting(
    audio_source: str,
    speaker_count: Optional[int] = None,
    language_code: str = "en",
    punctuate: bool = True,
    format_text: bool = True,
    is_local_file: bool = False,
    max_retries: int = 60,
    poll_interval_seconds: int = 5,
) -> TranscriptResponse:
    """
    Submit a recorded meeting for transcription with speaker diarization.

    Uses AssemblyAI Transcripts API with speaker_labels enabled. Optionally
    specifies the number of speakers if known.

    Args:
        audio_source: Publicly accessible URL or local file path to the meeting audio.
        speaker_count: Expected number of speakers (optional hint for AssemblyAI).
        language_code: ISO 639-1 language code.
        punctuate: Add punctuation to transcript.
        format_text: Format output text.
        is_local_file: If True, treat audio_source as a local file.
        max_retries: Maximum polling retries.
        poll_interval_seconds: Seconds between poll attempts.

    Returns:
        TranscriptResponse with speaker-labeled utterances.

    Raises:
        ValueError: If audio_source is empty or API key is missing.
        assemblyai.AssemblyAIError: If transcription fails.
        TimeoutError: If job does not complete within retry limit.
    """
    client = get_assemblyai_client()

    # Upload local file if needed
    if is_local_file:
        if not os.path.isfile(audio_source):
            raise ValueError(f"Local audio file not found: {audio_source}")
        audio_url = upload_local_audio(client, audio_source)
    else:
        audio_url = audio_source

    # Build config with speaker diarization enabled
    # AssemblyAI uses speaker_labels=True for diarization
    config = build_transcription_request(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,  # Enables AssemblyAI speaker diarization
        punctuate=punctuate,
        format_text=format_text,
    )

    # Submit the transcription job
    transcript = client.transcripts.submit(config=config)

    # Poll until completion
    raw_transcript = poll_with_retry(
        client=client,
        transcript_id=transcript.id,
        max_retries=max_retries,
        poll_interval_seconds=poll_interval_seconds,
    )

    # Normalize response
    response = normalize_assemblyai_response(raw_transcript)

    return response


def get_speaker_summary(transcript_response: TranscriptResponse) -> dict:
    """
    Generate a per-speaker summary from diarized transcript.

    Args:
        transcript_response: Normalized TranscriptResponse with utterances.

    Returns:
        Dictionary mapping speaker IDs to their statistics and text.
    """
    speakers = {}

    for utterance in transcript_response.utterances:
        speaker = utterance.speaker or "Unknown"

        if speaker not in speakers:
            speakers[speaker] = {
                "speaker_id": speaker,
                "utterance_count": 0,
                "total_text": [],
                "total_duration_ms": 0,
                "first_word": None,
                "last_word": None,
            }

        speakers[speaker]["utterance_count"] += 1
        speakers[speaker]["total_text"].append(utterance.text)

        if utterance.start_ms is not None:
            if speakers[speaker]["first_word"] is None or utterance.start_ms < speakers[speaker]["first_word"]:
                speakers[speaker]["first_word"] = utterance.start_ms
        if utterance.end_ms is not None:
            if speakers[speaker]["last_word"] is None or utterance.end_ms > speakers[speaker]["last_word"]:
                speakers[speaker]["last_word"] = utterance.end_ms
            speakers[speaker]["total_duration_ms"] += (utterance.end_ms - (utterance.start_ms or utterance.end_ms))

    # Convert text lists to full transcripts
    for speaker_id, data in speakers.items():
        data["full_text"] = " ".join(data["total_text"])
        del data["total_text"]

    return speakers


def format_diarized_transcript(transcript_response: TranscriptResponse) -> str:
    """
    Format a diarized transcript as a readable conversation.

    Args:
        transcript_response: Normalized TranscriptResponse with utterances.

    Returns:
        Formatted string showing speaker labels and their text.
    """
    lines = []
    for utterance in transcript_response.utterances:
        speaker = utterance.speaker or "Unknown"
        lines.append(f"[{speaker}] {utterance.text}")
    return "\n".join(lines)


def main():
    """CLI entry point for diarizing a meeting recording."""
    import argparse

    parser = argparse.ArgumentParser(description="Diarize a meeting recording with AssemblyAI")
    parser.add_argument("audio", help="Audio URL or local file path")
    parser.add_argument("--local", action="store_true", help="Treat audio as local file")
    parser.add_argument("--speakers", type=int, help="Expected number of speakers")
    parser.add_argument("--language", default="en", help="Language code")
    parser.add_argument("--summary", action="store_true", help="Show speaker summary")

    args = parser.parse_args()

    response = diarize_meeting(
        audio_source=args.audio,
        speaker_count=args.speakers,
        language_code=args.language,
        is_local_file=args.local,
    )

    if args.summary:
        summary = get_speaker_summary(response)
        print("=== Speaker Summary ===")
        for speaker_id, data in summary.items():
            print(f"\nSpeaker {speaker_id}: {data['utterance_count']} utterances")
            print(f"  Text: {data['full_text'][:200]}...")
    else:
        print("=== Diarized Transcript ===")
        print(format_diarized_transcript(response))

    return response


if __name__ == "__main__":
    main()
