import assemblyai as aai
import os


def get_assemblyai_client() -> aai.Client:
    """
    Provides local configuration and client helper utilities for AssemblyAI.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    return aai.Client(api_key)
