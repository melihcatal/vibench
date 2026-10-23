import os
import assemblyai

def get_speech_client():
    """
    Initializes and returns the AssemblyAI streaming transcriber client.
    Requires the ASSEMBLYAI_API_KEY environment variable to be set.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    transcriber = assemblyai.Transcriber()
    return transcriber
