import os
from assemblyai import Client, Transcriber
from speech_client import get_assemblyai_client

def submit_transcription_job(audio_url: str):
    """Submits an audio file for batch transcription using AssemblyAI."""
    client = get_assemblyai_client()
    config = {
        "audio_url": audio_url
    }
    transcript = client.transcripts.submit(config)
    return transcript.id

if __name__ == '__main__':
    # Example usage: Replace with a real audio URL
    audio_file_url = "https://example.com/audio.mp3"
    job_id = submit_transcription_job(audio_file_url)
    print(f"Submitted AssemblyAI transcription job with ID: {job_id}")
