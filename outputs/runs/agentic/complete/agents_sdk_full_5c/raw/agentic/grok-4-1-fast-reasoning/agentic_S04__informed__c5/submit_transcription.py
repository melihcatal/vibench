from speech_client import get_speech_client, upload_audio

def submit_transcription(audio_file_path: str) -> str:
    """
    Submit an audio file for batch transcription.
    Returns the job ID.
    """
    client = get_speech_client()
    audio_url = upload_audio(client, audio_file_path)
    transcript = client.transcripts.create(audio_url=audio_url)
    return transcript.id
