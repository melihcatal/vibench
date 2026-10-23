import os
import assemblyai as aai


def get_client():
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required.")
    aai.settings.api_key = api_key
    return aai.Client()
