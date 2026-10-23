import time
from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult


def poll_transcription_job(job_id: str) -> TranscriptionResult:
    """
    Polls an AssemblyAI transcription job until it's completed.
    """
    aai = get_assemblyai_client()
    transcriber = aai.Transcriber()
    transcript = transcriber.get_by_id(job_id)

    while transcript.status not in ["completed", "error"]:
        time.sleep(5)
        transcript = transcriber.get_by_id(transcript.id)

    return TranscriptionResult(
        id=transcript.id, status=transcript.status, text=transcript.text
    )
