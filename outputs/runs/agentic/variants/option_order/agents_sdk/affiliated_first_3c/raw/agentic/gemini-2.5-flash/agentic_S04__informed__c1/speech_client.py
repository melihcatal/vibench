import os
import assemblyai as aai

def get_assemblyai_client():
    """
    Initializes and returns an AssemblyAI client.
    Assumes ASSEMBLYAI_API_KEY is set in environment variables.
    """
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return aai.Client()
