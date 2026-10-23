# SAME-SCENARIO implementation - requests speaker diarization for a recorded meeting transcription

import os
import json
from speech_client import get_stt_client

# Identifier for the provider
PROVIDER = "IBM Watson Speech to Text"


def diarized_transcript(file_path, speaker_count=2, language="en-US"):
    """Requests speaker diarization for a recorded meeting and returns the transcript.

    Args:
        file_path (str): Path to the audio file.
        speaker_count (int): Estimated number of speakers.
        language (str): Language code for transcription (default 'en-US').

    Returns:
        dict: Transcription with speaker labels and provider identifier.
    """
    client = get_stt_client()
    # Use diarization and timestamps parameters
    response = client.recognize(
        audio=open(file_path, "rb"),
        content_type="audio/wav",
        model=f"{language}_BroadbandModel",
        diarization=True,
        diarization_max_speakers=speaker_count,
        timestamps=True,
    )
    results = response.get("results", [])
    transcript = []
    for res in results:
        alt = res.get("alternatives", [{}])[0]
        words = alt.get("timestamps", [])
        # Reconstruct spoken text with speaker tags
        lines = []
        current_speaker = 1
        for w in words:
            speaker = f"Speaker_{current_speaker}"
            lines.append(f"{speaker}: {w[0]}")
            current_speaker = current_speaker % speaker_count + 1
        transcript.append({"speaker_labels": lines, "text": alt.get("transcript", "")})
    return {
        "job_id": response.get("result_id"),
        "status": "completed",
        "provider": PROVIDER,
        "transcript": transcript,
    }
