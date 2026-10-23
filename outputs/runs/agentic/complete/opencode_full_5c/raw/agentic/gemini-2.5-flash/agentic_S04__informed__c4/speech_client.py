import os
import assemblyai as aai


def get_assemblyai_client():
    """Provides a configured AssemblyAI client."""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return aai.Client(api_key)
