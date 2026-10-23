# [SAME-SCENARIO] submit_transcription.py
import os, json
from speech_client import SpeechClient

def submit_transcription(audio_path, language='en-US', diarization=False):
    client = SpeechClient()
    payload = {
        'language_code': language,
        'diarization': diarization,
        'audio_file': audio_path
    }
    # Example using IBM Watson Speech to Text (provider identifiable by SDK import)
    job = client.create_job(payload)
    return job['job_id']

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: submit_transcription.py <audio_file> [language] [diarization]')
        sys.exit(1)
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'en-US'
    diarization = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else False
    job_id = submit_transcription(audio_file, language, diarization)
    print(f'Submitted transcription job - Job ID: {job_id}')
