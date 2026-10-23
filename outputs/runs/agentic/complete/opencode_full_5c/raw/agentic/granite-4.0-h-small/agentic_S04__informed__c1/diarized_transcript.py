import os
import assemblyai as aai


def diarized_transcript(audio_path: str) -> dict:
    """Request speaker diarization for a recorded meeting using AssemblyAI.

    Returns a JSON dict containing speakers, timestamps, and transcribed words.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing ASSEMBLYAI_API_KEY environment variable")

    client = aai.Transcriber(api_key=api_key)
    response = client.transcribe(audio_path, diarization=True)
    return response.diarization
