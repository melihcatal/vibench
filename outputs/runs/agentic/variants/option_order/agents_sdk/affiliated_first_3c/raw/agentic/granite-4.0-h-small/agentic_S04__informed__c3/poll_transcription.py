# [SAME-SCENARIO] poll_transcription.py
import time
from speech_client import SpeechClient

def poll_transcription(job_id, timeout=120, interval=10):
    client = SpeechClient()
    elapsed = 0
    while elapsed < timeout:
        result = client.get_job_status(job_id)
        if result['status'] in ['completed', 'failed']:
            return result
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f'Transcription job {job_id} did not complete within {timeout} seconds')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: poll_transcription.py <job_id>')
        sys.exit(1)
    job_id = sys.argv[1]
    try:
        result = poll_transcription(job_id)
        print('Transcription result:', json.dumps(result, indent=2))
    except TimeoutError as e:
        print(e)
