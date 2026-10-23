import os

def get_api_key() -> str:
    key = os.getenv("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set")
    return key
