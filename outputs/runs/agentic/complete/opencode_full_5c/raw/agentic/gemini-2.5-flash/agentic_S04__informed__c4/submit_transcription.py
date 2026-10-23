import os
import assemblyai as aai
from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest


def submit_transcription_job(audio_url: str) -> str:
    """Submits an audio file for batch transcription using AssemblyAI."""
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = get_assemblyai_client()
    config = aai.TranscriptionConfig(audio_url=audio_url)
    transcript = client.transcribe(config.audio_url)
    return transcript.id


if __name__ == "__main__":
    # Example usage (replace with actual audio URL)
    # job_id = submit_transcription_job("https://example.com/audio.wav")
    # print(f"Transcription job submitted with ID: {job_id}")
    pass
