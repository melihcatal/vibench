import os
import assemblyai as aai


def submit_transcription(audio_path: str) -> str:
    """Submit an audio file for batch transcription using AssemblyAI.

    Returns the UUID of the submitted transcription job.
    """
    # Load configuration via environment variable
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ASSEMBLYAI_API_KEY environment variable")

    client = aai.Transcriber(api_key=api_key)
    response = client.transcribe(audio_path)
    return response.id
