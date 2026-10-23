import os
import uuid
from speech_client import get_client
from speech_models import BatchTranscriptionConfig

# Constants for AssemblyAI
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

def submit_transcription(audio_path: str, transcript_id: str = None) -> dict:
    """Submit a batch transcription job to AssemblyAI.
    Returns the response JSON containing job metadata.
    """
    client = get_client()
    if transcript_id is None:
        transcript_id = str(uuid.uuid4())
    # AssemblyAI expects an audio URL—here we use a placeholder
    audio_url = f'file://{audio_path}'
    payload = {
        'audio_url': audio_url,
        'transcript_id': transcript_id,
        'config': {
            'd_phrase_detection': True,
            'diarize': True,
            'return_timestamps': True,
        }
    }
    response = client.Transcript.submit(payload)
    return response

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print('Usage: python submit_transcription.py <audio_file>')
        sys.exit(1)
    result = submit_transcription(sys.argv[1])
    print(result)
