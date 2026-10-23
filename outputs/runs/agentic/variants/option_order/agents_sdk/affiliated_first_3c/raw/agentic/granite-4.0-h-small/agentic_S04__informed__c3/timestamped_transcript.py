# [SAME-SCENARIO] timestamped_transcript.py
import json
from speech_client import SpeechClient

def get_timestamped_transcript(job_id):
    client = SpeechClient()
    result = client.get_job_status(job_id)
    if result['status'] != 'completed':
        raise RuntimeError('Job not completed yet')
    transcript = result.get('transcript', '')
    timestamps = result.get('timestamps', [])
    return transcript, timestamps

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: timestamped_transcript.py <job_id>')
        sys.exit(1)
    job_id = sys.argv[1]
    transcript, timestamps = get_timestamped_transcript(job_id)
    print('Transcript:', transcript)
    print('Timestamps:', json.dumps(timestamps, indent=2))
