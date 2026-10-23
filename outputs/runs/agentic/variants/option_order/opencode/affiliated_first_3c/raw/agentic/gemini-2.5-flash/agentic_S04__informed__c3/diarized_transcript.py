import os
from assemblyai import Client, TranscriptStatus


def get_diarized_transcript(transcript_id: str) -> dict:
    """
    Requests speaker diarization for a recorded meeting from an existing AssemblyAI transcript.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = Client(api_key=api_key)

    transcript = client.transcripts.get(transcript_id)

    if (
        transcript.status == TranscriptStatus.completed
        and transcript.speaker_diarization
    ):
        # The full transcript object already contains diarization if requested during submission
        return transcript.json()
    elif (
        transcript.status == TranscriptStatus.completed
        and not transcript.speaker_diarization
    ):
        # If diarization was not requested, we can't get it from an existing transcript without reprocessing.
        # For simplicity, this example assumes diarization was requested during submission.
        raise ValueError(
            "Transcript was not processed with speaker diarization enabled."
        )
    elif transcript.status == TranscriptStatus.error:
        raise RuntimeError(f"Transcription job failed: {transcript.error}")
    else:
        raise ValueError("Transcription job is not yet completed.")
