from speech_client import SpeechClient
from speech_models import TranscriptionRequest
import os


def submit_transcription_job(audio_url: str) -> str:
    client = SpeechClient()
    request = TranscriptionRequest(audio_url=audio_url)
    result = client.submit_transcription(request)
    return result.id


if __name__ == "__main__":
    # Example usage: Replace with an actual audio URL
    audio_file_url = os.getenv(
        "ASSEMBLYAI_AUDIO_URL",
        "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a",
    )
    job_id = submit_transcription_job(audio_file_url)
    print(f"Transcription job submitted with ID: {job_id}")
