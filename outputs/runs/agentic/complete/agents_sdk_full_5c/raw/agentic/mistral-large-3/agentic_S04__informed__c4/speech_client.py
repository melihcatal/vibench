import os
from assemblyai import TranscriptClient


def get_assemblyai_client() -> TranscriptClient:
    """
    Initialize and return an AssemblyAI client using the API key from environment variables.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
    return TranscriptClient(api_key=api_key)