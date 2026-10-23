from speech_client import get_assemblyai_client
from speech_models import TranscriptionResult
import assemblyai

def poll_for_transcript(job_id: str) -> TranscriptionResult:
    """
    Polls an AssemblyAI transcription job and returns the transcript text.
    """
    client = get_assemblyai_client()
    transcriber = client.transcriber
    
    transcript = transcriber.get_by_id(job_id)

    if transcript.status == assemblyai.TranscriptStatus.COMPLETED:
        return TranscriptionResult(
            job_id=transcript.id,
            status=transcript.status.value,
            text=transcript.text
        )
    elif transcript.status == assemblyai.TranscriptStatus.ERROR:
         return TranscriptionResult(
            job_id=transcript.id,
            status=transcript.status.value,
            text=transcript.error
        )
    else:
        return TranscriptionResult(
            job_id=transcript.id,
            status=transcript.status.value,
            text="Job is not yet complete."
        )
