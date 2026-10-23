from google.cloud import speech_v1p1beta1 as speech
from google.api_core.operations_v1 import OperationsClient

def create_speech_client(project_id: str, location: str) -> speech.SpeechClient:
    return speech.SpeechClient()