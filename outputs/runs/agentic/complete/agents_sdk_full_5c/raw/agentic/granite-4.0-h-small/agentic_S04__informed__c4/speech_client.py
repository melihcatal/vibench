import os
from assemblyai import AssemblyAI

# Expected environment variables: ASSEMBLYAI_API_KEY

def get_speech_client() -> AssemblyAI:
    """Return a configured AssemblyAI client for batch speech-to-text.
    AssemblyAI provides a simple SDK for transcription, diarization, timestamps, etc.
    """
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    if not api_key:
        raise RuntimeError('ASSEMBLYAI_API_KEY environment variable not set')
    return AssemblyAI(api_key)
