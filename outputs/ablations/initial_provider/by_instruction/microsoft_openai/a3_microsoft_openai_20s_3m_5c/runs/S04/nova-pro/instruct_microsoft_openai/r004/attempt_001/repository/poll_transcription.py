from speech_client import client
from speech_models import SpeechTranscriptionResponse

def poll_transcription(poller):
    result = poller.result()
    return SpeechTranscriptionResponse(result)