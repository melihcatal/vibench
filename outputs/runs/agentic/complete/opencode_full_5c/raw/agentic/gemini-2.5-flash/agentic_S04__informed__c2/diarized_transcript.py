import assemblyai
from speech_client import get_assemblyai_client


def request_diarized_transcript(audio_url: str) -> str:
    client = get_assemblyai_client()
    config = assemblyai.TranscriptionConfig(speaker_diarization=True)
    transcript = client.transcripts.submit(audio_url=audio_url, config=config)
    return transcript.id
