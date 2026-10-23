import assemblyai as aai
import os
from speech_client import get_assemblyai_client


def submit_transcription_job(audio_url: str) -> aai.Transcript:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    """
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = get_assemblyai_client()

    config = aai.TranscriptionConfig(
        speaker_diarization=True, sentiment_analysis=False, auto_chapters=False
    )
    transcript = client.transcripts.submit(audio_url=audio_url, config=config)
    return transcript
