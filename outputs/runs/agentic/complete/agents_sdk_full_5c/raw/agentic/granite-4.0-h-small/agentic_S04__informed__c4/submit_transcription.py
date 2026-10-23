import os, sys
from speech_client import get_speech_client

def submit_transcription(file_path, language='en-US'):
    """Submit a batch audio file for transcription.
    Returns the job ID for later polling.
    """
    client = get_speech_client()
    # Using AssemblyAI Transcripts API (REST)
    response = client.transcribe(file_path, language=language)
    # The API returns a JSON with a 'id' field representing the job ID
    job_id = response.get('id')
    if not job_id:
        raise RuntimeError('Failed to submit transcription: ' + str(response))
    print(f"Transcription job submitted. Job ID: {job_id}")
    return job_id

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: submit_transcription.py <path_to_audio_file>')
        sys.exit(1)
    path = sys.argv[1]
    submit_transcription(path)
