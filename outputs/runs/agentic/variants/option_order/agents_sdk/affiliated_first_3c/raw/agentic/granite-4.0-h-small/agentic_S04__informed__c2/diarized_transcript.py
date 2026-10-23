import os
from speech_client import get_client
from speech_models import BatchTranscriptionConfig

ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

def diarized_transcript(audio_path: str, transcript_id: str = None) -> dict:
    """Submit a batch transcription job with speaker diarization.
    Returns the response JSON containing the diarized transcript.
    """
    client = get_client()
    if transcript_id is None:
        transcript_id = str(uuid.uuid4())
    # AssemblyAI expects an audio URL—use a placeholder
    audio_url = f'file://{audio_path}'
    payload = {
        'audio_url': audio_url,
        'transcript_id': transcript_id,
        'config': {
            'diarize': True,
            'return_timestamps': True
        }
    }
    response = client.Transcript.submit(payload)
    return response

if __name__ == "__main__":
    import sys, uuid
    if len(sys.argv) != 2:
        print('Usage: python diarized_transcript.py <audio_file>')
        sys.exit(1)
    result = diarized_transcript(sys.argv[1])
    print(result)
