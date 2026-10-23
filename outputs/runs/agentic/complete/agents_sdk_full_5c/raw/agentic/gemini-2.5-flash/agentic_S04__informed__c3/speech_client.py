import os
import assemblyai as aai

def get_assemblyai_client():
    """Configures and returns an AssemblyAI client."""
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    return aai
