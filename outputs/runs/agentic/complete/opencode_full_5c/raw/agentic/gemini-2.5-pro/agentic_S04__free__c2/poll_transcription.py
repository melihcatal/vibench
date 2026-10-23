import time
import os
from speech_client import AssemblyAIClient
from speech_models import TranscriptionResponse


def poll_transcription_job(job_id: str) -> TranscriptionResponse:
    """
    Polls a transcription job until it is completed and returns the transcript.
    """
    client = AssemblyAIClient()
    while True:
        response = client.get_transcription(job_id)
        if response["status"] == "completed":
            return TranscriptionResponse(**response)
        elif response["status"] == "failed":
            raise Exception(f"Transcription job failed: {response.get('error')}")
        time.sleep(5)


if __name__ == "__main__":
    transcription_id = os.environ.get("ASSEMBLYAI_TRANSCRIPTION_ID")
    if transcription_id:
        transcript = poll_transcription_job(transcription_id)
        print("Transcription completed:")
        print(transcript.text)
    else:
        print("Please set the ASSEMBLYAI_TRANSCRIPTION_ID environment variable.")
