from speech_client import SpeechClient

client = SpeechClient()

def request_diarization(job_id):
    response = client.request_speaker_diarization(job_id)
    return response