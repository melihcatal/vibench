import os
from assemblyai import Client, PodParam, SpeechModel, TranscriptionConfig


def submit_transcription_job(audio_url: str) -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    client = Client(api_key=api_key)

    # Configure transcription with speaker diarization and word_boost
    config = TranscriptionConfig(
        speaker_diarization=True,
        word_boost=["AssemblyAI", "transcription", "AI"],
    )

    # Submit the transcription job
    transcript = client.transcripts.submit(
        audio=audio_url,
        config=config,
    )
    return transcript.id
