import os
from assemblyai import Client, Transcriber

def get_assemblyai_client() -> Client:
    """Provides a configured AssemblyAI client."""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return Client(api_key)
