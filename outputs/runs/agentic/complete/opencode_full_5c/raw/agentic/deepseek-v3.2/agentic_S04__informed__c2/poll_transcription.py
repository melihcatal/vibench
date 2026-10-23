import os
import time
import assemblyai as aai
from speech_client import get_assemblyai_client


def poll_transcription(job_id, timeout=300, poll_interval=5):
    """Poll a transcription job and return the transcript when complete."""
    client = get_assemblyai_client()

    start_time = time.time()

    while time.time() - start_time < timeout:
        transcript = client.transcript.get(job_id)

        if transcript.status == aai.TranscriptStatus.completed:
            return {
                "job_id": job_id,
                "status": "completed",
                "text": transcript.text,
                "words": [word.to_dict() for word in transcript.words]
                if transcript.words
                else [],
                "utterances": [utt.to_dict() for utt in transcript.utterances]
                if transcript.utterances
                else [],
                "provider": "AssemblyAI",
            }
        elif transcript.status == aai.TranscriptStatus.error:
            return {
                "job_id": job_id,
                "status": "error",
                "error": transcript.error,
                "provider": "AssemblyAI",
            }

        time.sleep(poll_interval)

    return {
        "job_id": job_id,
        "status": "timeout",
        "message": f"Transcription not completed within {timeout} seconds",
        "provider": "AssemblyAI",
    }
