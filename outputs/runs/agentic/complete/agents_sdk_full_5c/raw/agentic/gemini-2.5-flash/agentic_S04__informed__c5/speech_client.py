import os
import assemblyai

def get_assemblyai_client() -> assemblyai.Transcriber:
    """Provides a configured AssemblyAI Transcriber client."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    return assemblyai.Transcriber(api_key)

