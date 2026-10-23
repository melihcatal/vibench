import os
from assemblyai import Client, TranscriptStatus


def get_timestamped_transcript(transcript_id: str) -> dict:
    """
    Returns word or segment timestamps from an AssemblyAI transcription result.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = Client(api_key=api_key)

    transcript = client.transcripts.get(transcript_id)

    if transcript.status == TranscriptStatus.completed:
        return {
            "text": transcript.text,
            "words": [
                {
                    "text": word.text,
                    "start": word.start,
                    "end": word.end,
                    "speaker": word.speaker
                    if hasattr(word, "speaker")
                    else None,  # Include speaker if diarization is enabled
                }
                for word in transcript.words
            ],
        }
    elif transcript.status == TranscriptStatus.error:
        raise RuntimeError(f"Transcription job failed: {transcript.error}")
    else:
        raise ValueError("Transcription job is not yet completed.")
