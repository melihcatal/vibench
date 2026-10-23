import time
from speech_client import SpeechClient

client = SpeechClient()

def poll_transcription(job_id):
    while True:
        status = client.get_transcription_status(job_id)
        if status['status'] == 'completed':
            return client.get_transcription_result(job_id)
        elif status['status'] == 'failed':
            raise Exception('Transcription failed')
        time.sleep(5)