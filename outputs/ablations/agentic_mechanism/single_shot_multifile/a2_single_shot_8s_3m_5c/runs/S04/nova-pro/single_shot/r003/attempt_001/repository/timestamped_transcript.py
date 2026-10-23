from speech_client import SpeechClient

client = SpeechClient()

def get_timestamped_transcript(job_id):
    result = client.get_timestamped_transcript(job_id)
    return result['timestamped_transcript']