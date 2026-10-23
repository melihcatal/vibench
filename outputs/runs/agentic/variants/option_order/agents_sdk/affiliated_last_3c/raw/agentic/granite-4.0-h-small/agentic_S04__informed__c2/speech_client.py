import os
import assemblyai as aai

# Load API key from environment variable
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set")

# Initialise a single shared client instance
client = aai.TranscriptionClient(api_key=ASSEMBLYAI_API_KEY)

def audio_url_from_path(local_path: str):
    """If needed, upload audio file to a publicly accessible URL.
    For a simple demo we assume the path is already a URL or a temporary
    signed URL is generated externally.  You could integrate with a storage
    service (e.g., AWS S3, GCS) here to obtain a URL.
    """
    # Simple placeholder – return the local path directly for demo purposes
    return local_path
