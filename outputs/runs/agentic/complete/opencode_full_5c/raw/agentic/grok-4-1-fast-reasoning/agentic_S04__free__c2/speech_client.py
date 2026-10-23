import os
import assemblyai as aai


def get_client() -> aai.Client:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")
    return aai.Client(api_key=api_key)
