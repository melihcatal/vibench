import os
import assemblyai

def get_speech_client():
    """
    Configures and returns an AssemblyAI client.
    """
    assemblyai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    transcriber = assemblyai.Transcriber()
    return transcriber
