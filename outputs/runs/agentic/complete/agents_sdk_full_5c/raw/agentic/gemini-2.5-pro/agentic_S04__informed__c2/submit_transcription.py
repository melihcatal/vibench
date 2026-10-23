import os
from speech_client import get_speech_client

def submit_transcription_job(audio_url: str) -> str:
    """
    Submits a new transcription job to AssemblyAI.

    Args:
        audio_url: The public URL of the audio file to transcribe.

    Returns:
        The ID of the submitted transcription job.
    """
    client = get_speech_client()
    transcriber = client.Transcriber()
    
    config = client.TranscriptionConfig()
    
    job = transcriber.submit(audio_url, config)
    
    print(f"Submitted transcription job with ID: {job.id}")
    return job.id

if __name__ == '__main__':
    # This is an example of a public audio file
    audio_file_url = "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a"
    if "AUDIO_URL" in os.environ:
        audio_file_url = os.environ["AUDIO_URL"]
        
    submit_transcription_job(audio_file_url)
