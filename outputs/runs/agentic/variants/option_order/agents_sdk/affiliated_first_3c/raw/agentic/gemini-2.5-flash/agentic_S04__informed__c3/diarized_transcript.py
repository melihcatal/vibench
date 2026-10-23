import os
from assemblyai import Client, Transcriber
from speech_client import get_assemblyai_client

def submit_diarized_transcription(audio_url: str):
    """Submits an audio file for batch transcription with speaker diarization using AssemblyAI."""
    client = get_assemblyai_client()
    config = {
        "audio_url": audio_url,
        "speaker_diarization": True
    }
    transcript = client.transcripts.submit(config)
    return transcript.id

def get_diarized_transcript(job_id: str):
    """Retrieves a diarized transcript from AssemblyAI."""
    client = get_assemblyai_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status == Transcript.Status.completed:
        return transcript.text, transcript.json_response['words'] # Example of getting diarized words
    elif transcript.status == Transcript.Status.error:
        raise Exception(f"AssemblyAI diarization job {job_id} failed: {transcript.error}")
    else:
        return None, None

if __name__ == '__main__':
    # Example usage: Replace with a real audio URL
    audio_file_url = "https://example.com/meeting.mp3"
    job_id = submit_diarized_transcription(audio_file_url)
    print(f"Submitted AssemblyAI diarization job with ID: {job_id}")
    # In a real scenario, you would poll this job ID similar to poll_transcription.py
