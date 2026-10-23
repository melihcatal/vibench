from speech_client import SpeechClient
from speech_models import TranscriptionResult
import time


def poll_transcription_job(job_id: str) -> TranscriptionResult:
    client = SpeechClient()
    while True:
        result = client.poll_transcription(job_id)
        print(f"Polling job {job_id}. Current status: {result.status}")
        if result.status == "completed" or result.status == "error":
            return result
        time.sleep(5)  # Wait for 5 seconds before polling again


if __name__ == "__main__":
    # This part assumes a job_id is available from submit_transcription.py
    # For demonstration, let's use a placeholder or an actual completed job ID if known
    # job_id = "YOUR_TRANSCRIPTION_JOB_ID"
    # If running independently, you'd need a valid job ID.
    # For example, after running submit_transcription.py, take the job ID it prints.
    example_job_id = "_placeholder_job_id_"
    print(
        f"Please replace '{example_job_id}' with a real job ID from AssemblyAI to poll."
    )
    # transcript_result = poll_transcription_job(example_job_id)
    # if transcript_result.status == "completed":
    #     print("Transcription completed:")
    #     print(transcript_result.text)
    # else:
    #     print(f"Transcription job {example_job_id} failed with status: {transcript_result.status}")
