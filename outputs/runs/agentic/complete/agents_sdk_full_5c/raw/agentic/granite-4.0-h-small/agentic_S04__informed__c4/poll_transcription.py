import time, os
from speech_client import get_speech_client

def poll_transcription(job_id, poll_interval=10):
    """Poll a transcription job until completion and return the transcript.
    Returns the final transcript text.
    """
    client = get_speech_client()
    while True:
        status = client.get_job_status(job_id)
        if status.lower() == 'completed':
            result = client.get_job_result(job_id)
            transcript = result.get('transcript', '')
            print(f"Transcription completed. Transcript length: {len(transcript)} characters")
            return transcript
        elif status.lower() == 'failed':
            error = client.get_job_result(job_id)
            raise RuntimeError(f"Transcription job failed: {error}")
        else:
            print(f"Polling... Status: {status}. Waiting {poll_interval}s")
        time.sleep(poll_interval)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: poll_transcription.py <job_id>')
        sys.exit(1)
    job_id = sys.argv[1]
    transcript = poll_transcription(job_id)
    print("\nFinal Transcript:\n")
    print(transcript)
