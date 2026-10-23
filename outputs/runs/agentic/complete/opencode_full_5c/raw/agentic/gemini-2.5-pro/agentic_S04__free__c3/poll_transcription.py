import time
import os
from speech_client import get_assemblyai_client
from speech_models import TranscriptionResponse


def poll_transcription_job(job_id: str) -> TranscriptionResponse:
    """
    Polls a transcription job until it is completed.
    """
    client = get_assemblyai_client()
    while True:
        response_data = client.get_transcription(job_id)
        response = TranscriptionResponse(**response_data)
        if response.status == "completed":
            return response
        elif response.status == "failed":
            raise Exception(f"Transcription failed: {response.error}")
        time.sleep(5)


if __name__ == "__main__":
    # This is an example, replace with a real transcription ID from submit_transcription.py
    test_job_id = "your_transcription_id_here"
    if "ASSEMBLYAI_API_KEY" not in os.environ:
        print("Please set the ASSEMBLYAI_API_KEY environment variable.")
    elif test_job_id == "your_transcription_id_here":
        print("Please replace 'your_transcription_id_here' with a real job ID.")
    else:
        transcript = poll_transcription_job(test_job_id)
        print("Transcription completed:")
        print(transcript.text)
