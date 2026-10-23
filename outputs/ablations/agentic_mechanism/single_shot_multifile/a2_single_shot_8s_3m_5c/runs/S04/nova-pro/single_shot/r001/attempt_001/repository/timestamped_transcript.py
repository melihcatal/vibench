from speech_client import SpeechClient

client = SpeechClient()

def get_timestamped_transcript(job_id):
    response = client.get_transcription_result(job_id)
    return response['timestampedTranscript']