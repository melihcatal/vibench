import os
import assemblyai as aai
from speech_client import get_speech_client


def submit_transcription(audio_url: str, language_code: str = "en") -> str:
    """Submit an audio file for batch transcription using AssemblyAI."""
    client = get_speech_client()

    config = aai.TranscriptionConfig(
        language_code=language_code, speech_model=aai.SpeechModel.best
    )

    transcript = client.transcribe(audio_url, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    return transcript.id
