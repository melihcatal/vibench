import os
from speech_client import post_transcript


def submit_transcription_job(audio_file_url: str) -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    """
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        raise EnvironmentError("ASSEMBLYAI_API_KEY environment variable not set.")

    response = post_transcript(audio_file_url)
    return response.get("id")
