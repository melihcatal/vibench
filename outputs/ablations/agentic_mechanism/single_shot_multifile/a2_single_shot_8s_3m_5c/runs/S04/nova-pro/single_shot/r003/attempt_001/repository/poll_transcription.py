from speech_client import SpeechClient

client = SpeechClient()

def poll_transcription(job_id):
    result = client.poll_transcription_job(job_id)
    return result['transcript']