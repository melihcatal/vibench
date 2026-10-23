import os
import assemblyai

def get_speech_client():
    """
    Initializes and returns the AssemblyAI client using an API key
    from the environment variables.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    assemblyai.settings.api_key = api_key
    return assemblyai

