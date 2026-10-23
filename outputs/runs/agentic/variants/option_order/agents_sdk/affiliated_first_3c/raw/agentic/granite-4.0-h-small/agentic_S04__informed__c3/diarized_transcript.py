# [SAME-SCENARIO] diarized_transcript.py
import json
from speech_client import SpeechClient

def diarized_transcription(audio_path, language='en-US'):
    client = SpeechClient()
    payload = {
        'language_code': language,
        'diarization': True,
        'audio_file': audio_path
    }
    job_id = client.submit_batch_transcription(payload)
    print(f'Submitted diarized job ID: {job_id}')
    return job_id

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: diarized_transcript.py <audio_file>')
        sys.exit(1)
    audio_file = sys.argv[1]
    job_id = diarized_transcription(audio_file)
