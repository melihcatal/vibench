import os
import assemblyai

def get_assemblyai_client():
    """Initializes and returns the AssemblyAI client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return assemblyai.Client(api_key)
