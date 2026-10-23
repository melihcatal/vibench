"""
[SAME-SCENARIO] Submit an audio file for batch transcription via AssemblyAI.

Uploads audio and submits a transcription job using the AssemblyAI Transcripts API.
Provider: AssemblyAI Transcripts API
SDK: assemblyai
Auth: ASSEMBLYAI_API_KEY
"""

import os
import sys
from typing import Optional

from speech_client import get_assemblyai_client, build_transcription_request, upload_local_audio


def submit_transcription(
    audio_source: str,
    language_code: str = "en",
    punctuate: bool = True,
    format_text: bool = True,
    auto_chapters: bool = False,
    content_safety: bool = False,
    word_boost: Optional[list] = None,
    is_local_file: bool = False,
) -> str:
    """
    Submit an audio file for batch transcription using AssemblyAI.

    Args:
        audio_source: Publicly accessible URL or local file path to the audio.
        language_code: ISO 639-1 language code (default: 'en').
        punctuate: Whether to add punctuation to the transcript.
        format_text: Whether to format the output text.
        auto_chapters: Enable automatic chapter detection.
        content_safety: Enable content safety labeling.
        word_boost: List of words/phrases to boost detection confidence.
        is_local_file: If True, treat audio_source as a local file path and upload first.

    Returns:
        The AssemblyAI transcript ID for the submitted job.

    Raises:
        ValueError: If audio_source is empty or API key is missing.
        assemblyai.AssemblyAIError: If submission fails.
    """
    client = get_assemblyai_client()

    # If the audio is a local file, upload it to AssemblyAI first
    if is_local_file:
        if not os.path.isfile(audio_source):
            raise ValueError(f"Local audio file not found: {audio_source}")
        audio_url = upload_local_audio(client, audio_source)
    else:
        audio_url = audio_source

    # Build the transcription configuration
    config = build_transcription_request(
        audio_url=audio_url,
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
        auto_chapters=auto_chapters,
        content_safety=content_safety,
        word_boost=word_boost,
    )

    # Submit the transcription job via AssemblyAI SDK
    transcript = client.transcripts.submit(config=config)

    return transcript.id


def main():
    """CLI entry point for submitting a transcription job."""
    import argparse

    parser = argparse.ArgumentParser(description="Submit audio for AssemblyAI batch transcription")
    parser.add_argument("audio", help="Audio URL or local file path")
    parser.add_argument("--local", action="store_true", help="Treat audio as local file")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--chapters", action="store_true", help="Enable auto chapters")
    parser.add_argument("--safety", action="store_true", help="Enable content safety")
    parser.add_argument("--boost", nargs="*", help="Words to boost")

    args = parser.parse_args()

    transcript_id = submit_transcription(
        audio_source=args.audio,
        language_code=args.language,
        auto_chapters=args.chapters,
        content_safety=args.safety,
        word_boost=args.boost,
        is_local_file=args.local,
    )

    print(f"Transcription submitted. ID: {transcript_id}")
    return transcript_id


if __name__ == "__main__":
    main()
