import os
from azure.cognitiveservices.speech.transcription import TranscriptionClient
from azure.cognitiveservices.speech.transcription.models import TranscriptionProperties

speech_key = os.getenv('AZURE_SPEECH_KEY')
speech_region = os.getenv('AZURE_SPEECH_REGION')

transcription_client = TranscriptionClient(speech_key, speech_region)

def poll_transcription(transcription_id):
    transcription_properties = TranscriptionProperties(transcription_id=transcription_id)
    transcription_result = transcription_client.get_transcription(transcription_properties)
    return transcription_result.text