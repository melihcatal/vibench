import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

def get_transcriber():
    """Returns a configured AssemblyAI RealtimeTranscriber."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")
    
    aai.settings.api_key = api_key
    transcriber = aai.RealtimeTranscriber()
    return transcriber
