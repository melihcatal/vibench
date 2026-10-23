import os
import assemblyai as aai

def configure_assemblyai():
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required.")
    aai.settings.api_key = api_key