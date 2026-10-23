import os
import json
from speech_client import SpeechClient

# Config (env var or config file)
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

def submit_transcription(file_path):
    client = SpeechClient()  # helper returns configured client
    response = client.transcribe(file_path, api_key=ASSEMBLYAI_API_KEY)
    job_id = response.get('job_id')
    if not job_id:
        raise RuntimeError(f"Submission failed: {response}")
    print(f"Transcription submitted, job ID: {job_id}")
    return job_id

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Submit audio file for batch transcription.')
    parser.add_argument('file', help='Path to audio file (wav, mp3, etc.)')
    args = parser.parse_args()
    submit_transcription(args.file)
