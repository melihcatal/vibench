import os
import assemblyai as aai

def get_assemblyai_client() -> aai.Transcriber:
    """Initializes and returns an AssemblyAI Transcriber client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    aai.settings.api_key = api_key
    return aai.Transcriber()

def get_assemblyai_api_key() -> str:
    """Returns the AssemblyAI API key from environment variables."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return api_key
