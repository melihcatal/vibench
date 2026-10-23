import assemblyai as aai
from speech_client import get_speech_client

def submit_transcription(audio_file_path: str) -> str:
    client = get_speech_client()
    audio_url = client.upload(audio_file_path)
    config = aai.TranscriptionConfig(audio_url=audio_url)
    transcript = client.transcripts.create(config=config)
    return transcript.id