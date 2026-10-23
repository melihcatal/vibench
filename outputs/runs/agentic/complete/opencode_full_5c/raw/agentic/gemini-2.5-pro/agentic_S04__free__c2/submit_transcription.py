import os
from speech_client import AssemblyAIClient


def submit_transcription_job(audio_url: str) -> str:
    """
    Submits a new transcription job to AssemblyAI.
    """
    client = AssemblyAIClient()
    response = client.submit_transcription(audio_url)
    return response.get("id")


if __name__ == "__main__":
    audio_file_url = os.environ.get("EXAMPLE_AUDIO_URL")
    if audio_file_url:
        job_id = submit_transcription_job(audio_file_url)
        print(f"Transcription job submitted with ID: {job_id}")
    else:
        print("Please set the EXAMPLE_AUDIO_URL environment variable.")
