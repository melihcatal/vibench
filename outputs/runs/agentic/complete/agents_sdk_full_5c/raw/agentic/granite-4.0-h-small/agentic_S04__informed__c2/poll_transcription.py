import os
import assemblyai as aai
time import time

# Load credentials
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')

client = aai.Transcriber(ACCESS_TOKEN=ASSEMBLYAI_API_KEY)

def poll_transcription(job_id, poll_interval=5):
    """Poll a Batch Transcription job until it is completed.

    Returns the final transcript text (as a string).
    """
    while True:
        result = client.get_transcription(job_id)
        status = result.get('status')
        if status == 'queued':
            print(f"Job still queued...")
        elif status == 'processing':
            print(f"Job still processing...")
        elif status == 'completed':
            transcript = result.get('text')
            print('Transcription succeeded.')
            return transcript
        elif status in ('error', 'failed'):
            error_msg = result.get('error', {}).get('message', 'unknown error')
            print('Transcription failed:', error_msg)
            raise RuntimeError('Transcription failed')
        else:
            print('Unexpected status:', status)
        time.sleep(poll_interval)
