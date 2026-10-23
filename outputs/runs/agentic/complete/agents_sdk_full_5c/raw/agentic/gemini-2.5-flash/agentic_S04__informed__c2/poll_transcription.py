import os
import assemblyai as aai
from speech_models import TranscriptionResult

def poll_transcription(job_id: str) -> TranscriptionResult or None:
    """Polls a transcription job and returns the transcript if completed."""
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript_by_id(job_id)

    if transcript.status == aai.TranscriptStatus.completed:
        return TranscriptionResult(text=transcript.text, status=transcript.status.value)
    elif transcript.status == aai.TranscriptStatus.failed:
        raise Exception(f"Transcription job {job_id} failed: {transcript.error}")
    
    return TranscriptionResult(text=None, status=transcript.status.value)

if __name__ == "__main__":
    # Example usage (replace with actual job ID)
    # example_job_id = "your_assemblyai_job_id"
    # result = poll_transcription(example_job_id)
    # if result and result.text:
    #     print(f"Transcription completed:\n{result.text}")
    # else:
    #     print(f"Transcription status: {result.status if result else 'UNKNOWN'}")
    pass
